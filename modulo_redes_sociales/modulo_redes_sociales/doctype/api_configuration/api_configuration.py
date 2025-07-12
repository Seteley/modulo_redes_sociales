# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union


class APIConfiguration(Document):
    def validate(self) -> None:
        """Validar la configuración de la API"""
        if not self.api_url:
            frappe.throw("URL de la API es requerida")
        
        if not self.api_url.startswith(('http://', 'https://')):
            frappe.throw("URL de la API debe comenzar con http:// o https://")

    def test_api_connection(self) -> Dict[str, Any]:
        """Probar la conexión con la API externa"""
        try:
            # Verificar que los campos requeridos estén presentes
            if not self.api_url:
                return {"success": False, "error": "URL de API no configurada"}
            if not self.username:
                return {"success": False, "error": "Usuario no configurado"}
            if not self.get_password("password"):
                return {"success": False, "error": "Contraseña no configurada"}
            
            # Ajustar URL para conectividad WSL → Windows
            api_url = self.api_url
            if "localhost:8000" in api_url:
                # Intentar diferentes IPs para WSL → Windows
                test_urls = [
                    api_url,  # URL original
                    api_url.replace("localhost", "172.25.128.1"),
                    api_url.replace("localhost", "host.docker.internal"),
                    api_url.replace("localhost", "172.25.132.112")
                ]
            else:
                test_urls = [api_url]
            
            # Probar cada URL hasta que una funcione
            response = None
            working_url = None
            for test_url in test_urls:
                try:
                    login_url = f"{test_url.rstrip('/')}/auth/login"
                    login_data = {
                        "username": self.username,
                        "password": self.get_password("password")
                    }
                    
                    # Realizar login
                    response = requests.post(
                        login_url,
                        json=login_data,
                        timeout=self.timeout or 10  # Timeout más corto para probar múltiples URLs
                    )
                    
                    if response.status_code == 200:
                        working_url = test_url
                        break
                        
                except requests.exceptions.RequestException:
                    continue
            
            if not response or response.status_code != 200:
                self.connection_status = "Fallido"
                self.last_connection_test = datetime.now()
                return {"success": False, "error": "No se pudo conectar con la API"}
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            if access_token:
                # Guardar el token
                self.access_token = access_token
                # Establecer expiración (típicamente 1 hora)
                self.token_expiry = datetime.now() + timedelta(hours=1)
                self.connection_status = "Exitoso"
                self.last_connection_test = datetime.now()
                
                # Actualizar URL si se usó una alternativa
                if working_url != self.api_url:
                    message = f"Conexión exitosa usando URL alternativa: {working_url}"
                else:
                    message = "Conexión exitosa con la API"
                
                return {"success": True, "message": message}
            else:
                self.connection_status = "Fallido"
                self.last_connection_test = datetime.now()
                return {"success": False, "error": "No se pudo obtener el token de acceso"}
                
        except requests.exceptions.Timeout:
            self.connection_status = "Fallido"
            self.last_connection_test = datetime.now()
            return {"success": False, "error": "Timeout al conectar con la API"}
        except requests.exceptions.ConnectionError:
            self.connection_status = "Fallido"
            self.last_connection_test = datetime.now()
            return {"success": False, "error": "Error de conexión con la API"}
        except Exception as e:
            self.connection_status = "Fallido"
            self.last_connection_test = datetime.now()
            return {"success": False, "error": f"Error inesperado: {str(e)}"}

    def get_valid_token(self) -> Optional[str]:
        """Obtener un token válido, renovándolo si es necesario"""
        if not self.access_token or not self.token_expiry:
            self.test_api_connection()
            return self.access_token
        
        # Verificar si el token está por expirar (renovar 5 minutos antes)
        if datetime.now() + timedelta(minutes=5) > self.token_expiry:
            self.test_api_connection()
        
        return self.access_token

    def make_api_request(self, endpoint: str, method: str = "GET", 
                        data: Optional[Dict[str, Any]] = None, 
                        params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Realizar una petición a la API con reintentos automáticos optimizados"""
        
        # Log inicial para debug
        frappe.log_error(f"[API CONFIG] Iniciando make_api_request: endpoint={endpoint}, method={method}", "Social Media API Debug")
        
        token = self.get_valid_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        frappe.log_error(f"[API CONFIG] URL construida: {url}", "Social Media API Debug")
        frappe.log_error(f"[API CONFIG] Headers: Authorization=Bearer {token[:20]}... Content-Type=application/json", "Social Media API Debug")
        
        # Valores optimizados para desarrollo
        max_retries = 2  # Reducido de 3 a 2
        retry_delay = 0.5  # Reducido de 5s a 0.5s
        timeout = 10  # Reducido de 30s a 10s
        
        for attempt in range(max_retries + 1):
            try:
                # Log detallado para debug
                frappe.log_error(f"API Request attempt {attempt + 1}: {method} {url}", "Social Media API Debug")
                if params:
                    frappe.log_error(f"API Request params: {params}", "Social Media API Debug")
                if data:
                    frappe.log_error(f"API Request data: {data}", "Social Media API Debug")
                
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers, params=params, timeout=timeout)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=headers, json=data, timeout=timeout)
                elif method.upper() == "PUT":
                    response = requests.put(url, headers=headers, json=data, timeout=timeout)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, headers=headers, timeout=timeout)
                else:
                    frappe.throw(f"Método HTTP no soportado: {method}")
                
                # Log de respuesta para debug - limitado para evitar truncamiento
                if response.status_code in [200, 201, 204]:
                    frappe.log_error(f"API Response: {response.status_code} - Success", "Social Media API Debug")
                else:
                    # Solo mostrar primeros 100 caracteres del error
                    error_text = response.text[:100] + "..." if len(response.text) > 100 else response.text
                    frappe.log_error(f"API Response: {response.status_code} - {error_text}", "Social Media API Debug")
                
                # Si la respuesta es exitosa, devolverla
                if response.status_code in [200, 201, 204]:
                    return response.json() if response.content else {}
                
                # Si es error de autenticación, intentar renovar token
                elif response.status_code == 401:
                    if attempt == 0:  # Solo intentar renovar token en el primer intento
                        self.test_api_connection()
                        token = self.access_token
                        headers["Authorization"] = f"Bearer {token}"
                        continue
                    else:
                        frappe.throw("Error de autenticación: Token inválido")
                
                # Para otros errores, lanzar excepción
                else:
                    # Limitar longitud del mensaje de error
                    error_text = response.text[:100] + "..." if len(response.text) > 100 else response.text
                    frappe.throw(f"Error de API: {response.status_code} - {error_text}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    # Log simple sin detalles excesivos
                    frappe.log_error(f"Timeout en intento {attempt + 1}, reintentando en {retry_delay}s", "API Timeout")
                    import time
                    time.sleep(retry_delay)
                    continue
                else:
                    frappe.throw("Timeout en todos los intentos de conexión")
                    
            except requests.exceptions.ConnectionError:
                if attempt < max_retries:
                    # Log simple sin detalles excesivos
                    frappe.log_error(f"Error de conexión en intento {attempt + 1}, reintentando en {retry_delay}s", "API Connection")
                    import time
                    time.sleep(retry_delay)
                    continue
                else:
                    frappe.throw("Error de conexión en todos los intentos")
                    
            except Exception as e:
                # Limitar longitud del mensaje de error
                error_msg = str(e)
                if len(error_msg) > 100:
                    error_msg = error_msg[:100] + "... (truncado)"
                # Log sin usar frappe.log_error para evitar bucles
                frappe.throw(f"Error inesperado: {error_msg}")

    @frappe.whitelist()
    def test_connection_btn(self) -> None:
        """Método para el botón de probar conexión"""
        result = self.test_api_connection()
        
        # Guardar los cambios de estado
        try:
            self.save()
        except:
            # En caso de que no se pueda guardar, continuar
            pass
        
        if result.get("success"):
            frappe.msgprint(result.get("message", "Conexión exitosa"))
        else:
            frappe.throw(result.get("error", "Error en la conexión"))
        
        return result


@frappe.whitelist()
def get_api_configuration():
    """Obtener la configuración de API activa"""
    config = frappe.get_list("API Configuration", 
                           filters={"enabled": 1}, 
                           limit=1)
    if config:
        return frappe.get_doc("API Configuration", config[0].name)
    return None

@frappe.whitelist()
def test_connection(api_config_name):
    """Método whitelist para probar conexión desde otros DocTypes"""
    try:
        if not api_config_name:
            return {"success": False, "error": "No se proporcionó el nombre de la configuración de API"}
        
        # Obtener el documento de API Configuration
        api_config = frappe.get_doc("API Configuration", api_config_name)
        
        # Probar la conexión
        result = api_config.test_api_connection()
        
        if result:
            return {"success": True, "message": "Conexión exitosa con la API"}
        else:
            return {"success": False, "error": "Error en la conexión"}
            
    except frappe.DoesNotExistError:
        return {"success": False, "error": f"La configuración de API '{api_config_name}' no existe"}
    except Exception as e:
        frappe.log_error(f"Error al probar conexión API: {str(e)}")
        return {"success": False, "error": str(e)}
