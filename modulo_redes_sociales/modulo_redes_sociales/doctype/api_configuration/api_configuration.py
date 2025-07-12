# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from datetime import datetime, timedelta


class APIConfiguration(Document):
    def validate(self):
        """Validar la configuración de la API"""
        if not self.api_url:
            frappe.throw("URL de la API es requerida")
        
        if not self.api_url.startswith(('http://', 'https://')):
            frappe.throw("URL de la API debe comenzar con http:// o https://")

    def test_api_connection(self):
        """Probar la conexión con la API externa"""
        try:
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
                        # Esta URL funciona, actualizar la configuración
                        if test_url != self.api_url:
                            frappe.msgprint(f"Conectado usando URL alternativa: {test_url}")
                            # Opcionalmente actualizar la URL en la configuración
                            # self.api_url = test_url
                        break
                except requests.exceptions.RequestException:
                    continue
            else:
                # Si ninguna URL funcionó
                raise requests.exceptions.ConnectionError("No se pudo conectar con ninguna URL")
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                
                if access_token:
                    # Guardar el token
                    self.access_token = access_token
                    # Establecer expiración (típicamente 1 hora)
                    self.token_expiry = datetime.now() + timedelta(hours=1)
                    self.connection_status = "Exitoso"
                    self.last_connection_test = datetime.now()
                    
                    frappe.msgprint("Conexión exitosa con la API")
                    return True
                else:
                    self.connection_status = "Fallido"
                    self.last_connection_test = datetime.now()
                    frappe.throw("No se pudo obtener el token de acceso")
            else:
                self.connection_status = "Fallido"
                self.last_connection_test = datetime.now()
                frappe.throw(f"Error en login: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            self.connection_status = "Fallido"
            self.last_connection_test = datetime.now()
            frappe.throw("Timeout al conectar con la API")
        except requests.exceptions.ConnectionError:
            self.connection_status = "Fallido"
            self.last_connection_test = datetime.now()
            frappe.throw("Error de conexión con la API")
        except Exception as e:
            self.connection_status = "Fallido"
            self.last_connection_test = datetime.now()
            frappe.throw(f"Error inesperado: {str(e)}")

    def get_valid_token(self):
        """Obtener un token válido, renovándolo si es necesario"""
        if not self.access_token or not self.token_expiry:
            self.test_api_connection()
            return self.access_token
        
        # Verificar si el token está por expirar (renovar 5 minutos antes)
        if datetime.now() + timedelta(minutes=5) > self.token_expiry:
            self.test_api_connection()
        
        return self.access_token

    def make_api_request(self, endpoint, method="GET", data=None, params=None):
        """Realizar una petición a la API con reintentos automáticos"""
        token = self.get_valid_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        max_retries = self.max_retries or 3
        retry_delay = self.retry_delay or 5
        
        for attempt in range(max_retries + 1):
            try:
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers, params=params, timeout=self.timeout or 30)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=headers, json=data, timeout=self.timeout or 30)
                elif method.upper() == "PUT":
                    response = requests.put(url, headers=headers, json=data, timeout=self.timeout or 30)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, headers=headers, timeout=self.timeout or 30)
                else:
                    frappe.throw(f"Método HTTP no soportado: {method}")
                
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
                    frappe.throw(f"Error de API: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    frappe.log_error(f"Timeout en intento {attempt + 1}, reintentando en {retry_delay}s")
                    import time
                    time.sleep(retry_delay)
                    continue
                else:
                    frappe.throw("Timeout en todos los intentos de conexión")
                    
            except requests.exceptions.ConnectionError:
                if attempt < max_retries:
                    frappe.log_error(f"Error de conexión en intento {attempt + 1}, reintentando en {retry_delay}s")
                    import time
                    time.sleep(retry_delay)
                    continue
                else:
                    frappe.throw("Error de conexión en todos los intentos")
                    
            except Exception as e:
                frappe.log_error(f"Error inesperado: {str(e)}")
                frappe.throw(f"Error inesperado: {str(e)}")

    @frappe.whitelist()
    def test_connection_btn(self):
        """Método para el botón de probar conexión"""
        return self.test_api_connection()


@frappe.whitelist()
def get_api_configuration():
    """Obtener la configuración de API activa"""
    config = frappe.get_list("API Configuration", 
                           filters={"enabled": 1}, 
                           limit=1)
    if config:
        return frappe.get_doc("API Configuration", config[0].name)
    return None
