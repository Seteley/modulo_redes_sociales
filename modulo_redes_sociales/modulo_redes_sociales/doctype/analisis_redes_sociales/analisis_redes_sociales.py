# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime
from typing import Dict, Any, Optional, Union


class AnalisisRedesSociales(Document):
    def validate(self) -> None:
        """Validar los parámetros del análisis"""
        # Validar que hay una configuración de API seleccionada
        if not self.api_configuration:
            frappe.throw("Debe seleccionar una Configuración de API")
        
        # Validar que la configuración de API existe y está habilitada
        api_config = frappe.get_doc("API Configuration", self.api_configuration)
        if not api_config.enabled:
            frappe.throw(f"La configuración de API '{self.api_configuration}' no está habilitada")
        
        if self.tipo_analisis == "Predicción de Seguidores":
            if not self.fecha_analisis:
                frappe.throw("Para predicción de seguidores se requiere una fecha de análisis")
        
        elif self.tipo_analisis == "Clustering":
            if not all([self.likes, self.comentarios, self.compartidos]):
                frappe.throw("Para clustering se requieren likes, comentarios y compartidos")

    def after_insert(self) -> None:
        """Ejecutar después de insertar el documento"""
        if self.estado == "Pendiente":
            # Auto-ejecutar el análisis después de guardar
            frappe.enqueue(
                method='modulo_redes_sociales.modulo_redes_sociales.doctype.analisis_redes_sociales.analisis_redes_sociales._ejecutar_analisis_background',
                queue='default',
                timeout=300,
                is_async=True,
                docname=self.name
            )

    def _ejecutar_prediccion(self, config_doc) -> Dict[str, Any]:
        """Ejecutar predicción de seguidores"""
        if not self.fecha_analisis:
            raise Exception("Fecha de análisis requerida para predicción")
        
        # Preparar parámetros de query según la documentación de la API
        params = {
            "fecha": self.fecha_analisis.strftime("%Y-%m-%d")
        }
        
        # Log para debug
        self.log_ejecucion += f"\n[DEBUG] Endpoint: regression/predict/{self.usuario_red_social}"
        self.log_ejecucion += f"\n[DEBUG] Método: GET"
        self.log_ejecucion += f"\n[DEBUG] Parámetros: {params}"
        self.log_ejecucion += f"\n[DEBUG] URL completa: {config_doc.api_url}/regression/predict/{self.usuario_red_social}?fecha={params['fecha']}"
        self.log_ejecucion += f"\n[DEBUG] Config API URL: {config_doc.api_url}"
        self.log_ejecucion += f"\n[DEBUG] Config API Name: {config_doc.api_name}"
        
        # Guardar log antes de hacer el request
        self.save()
        frappe.db.commit()
        
        # El endpoint correcto según la documentación: /regression/predict/{username}?fecha=YYYY-MM-DD
        endpoint = f"regression/predict/{self.usuario_red_social}"
        
        # Log antes del request
        frappe.log_error(f"[PREDICCION DEBUG] Calling make_api_request with: endpoint={endpoint}, method=GET, params={params}", "Social Media Prediccion")
        
        try:
            # Usar GET con parámetros, no POST con data
            result = config_doc.make_api_request(endpoint, method="GET", params=params)
            self.log_ejecucion += f"\n[DEBUG] Request exitoso, resultado: {str(result)[:200]}"
            return result
        except Exception as e:
            self.log_ejecucion += f"\n[DEBUG] Error en make_api_request: {str(e)}"
            frappe.log_error(f"[PREDICCION ERROR] {str(e)}", "Social Media Prediccion")
            raise e

    def _ejecutar_clustering(self, config_doc):
        """Ejecutar clustering de publicaciones"""
        data = {
            "likes": self.likes,
            "comentarios": self.comentarios,
            "compartidos": self.compartidos
        }
        
        endpoint = f"clustering/predict/{self.usuario_red_social}"
        return config_doc.make_api_request(endpoint, method="POST", data=data)

    def _ejecutar_entrenamiento(self, config_doc):
        """Ejecutar entrenamiento de modelo"""
        endpoint = f"regression/train/{self.usuario_red_social}"
        return config_doc.make_api_request(endpoint)

    def _obtener_metricas(self, config_doc):
        """Obtener métricas del modelo"""
        endpoint = f"regression/metrics/{self.usuario_red_social}"
        return config_doc.make_api_request(endpoint)

    def _procesar_resultados(self, result):
        """Procesar los resultados del análisis"""
        try:
            if not result:
                raise Exception("Resultado vacío de la API")
            
            # Log del resultado recibido
            self.log_ejecucion += f"\nResultado recibido: {json.dumps(result, indent=2)}"
            
            if self.tipo_analisis == "Predicción de Seguidores":
                if "prediction" in result:
                    self.prediccion_seguidores = result["prediction"]
                elif "prediccion" in result:
                    self.prediccion_seguidores = result["prediccion"]
                else:
                    self.log_ejecucion += "\nAdvertencia: No se encontró predicción en el resultado"

            elif self.tipo_analisis == "Clustering":
                if "cluster" in result:
                    self.cluster_asignado = result["cluster"]
                if "cluster_name" in result:
                    self.cluster_nombre = result["cluster_name"]
                elif "nombre_cluster" in result:
                    self.cluster_nombre = result["nombre_cluster"]

            elif self.tipo_analisis == "Entrenamiento de Modelo":
                metricas = {}
                if "model_id" in result:
                    self.modelo_usado = result["model_id"]
                    metricas["model_id"] = result["model_id"]
                if "r2_score" in result:
                    metricas["r2_score"] = result["r2_score"]
                if "mae" in result:
                    metricas["mae"] = result["mae"]
                if "rmse" in result:
                    metricas["rmse"] = result["rmse"]
                
                self.metricas_modelo = json.dumps(metricas, indent=2)

            elif self.tipo_analisis == "Métricas de Modelo":
                metricas = {}
                if "r2" in result:
                    metricas["r2"] = result["r2"]
                if "mae" in result:
                    metricas["mae"] = result["mae"]
                if "rmse" in result:
                    metricas["rmse"] = result["rmse"]
                
                self.metricas_modelo = json.dumps(metricas, indent=2)
                    
        except Exception as e:
            self.log_ejecucion += f"\nError procesando resultados: {str(e)}"
            raise e

    @frappe.whitelist()
    def reejecutar_analisis(self):
        """Re-ejecutar el análisis"""
        self.estado = "Pendiente"
        self.error_message = ""
        self.save()
        
        frappe.enqueue(
            method='modulo_redes_sociales.modulo_redes_sociales.doctype.analisis_redes_sociales.analisis_redes_sociales._ejecutar_analisis_background',
            queue='default',
            timeout=300,
            is_async=True,
            docname=self.name
        )
        
        frappe.msgprint("Análisis en cola para re-ejecución")


# Funciones globales (whitelist)

@frappe.whitelist()
def ejecutar_analisis(docname):
    """Función global para ejecutar análisis desde JavaScript"""
    return _ejecutar_analisis_background(docname)


def _ejecutar_analisis_background(docname):
    """Ejecutar análisis en background (función global para enqueue)"""
    start_time = datetime.now()
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", docname)
        doc.estado = "Ejecutando"
        doc.log_ejecucion = f"[{start_time.strftime('%H:%M:%S.%f')[:-3]}] Iniciando análisis..."
        doc.save()
        frappe.db.commit()

        # Obtener configuración de API desde el campo del documento
        if not doc.api_configuration:
            raise Exception("No hay configuración de API seleccionada")
        
        # Verificar que la configuración existe
        if not frappe.db.exists("API Configuration", doc.api_configuration):
            raise Exception(f"La configuración de API '{doc.api_configuration}' no existe")
        
        config_doc = frappe.get_doc("API Configuration", doc.api_configuration)
        
        # Verificar que la configuración está habilitada
        if not config_doc.enabled:
            raise Exception(f"La configuración de API '{doc.api_configuration}' no está habilitada")
        
        # Log del intento de conexión
        connect_time = datetime.now()
        doc.log_ejecucion += f"\n[{connect_time.strftime('%H:%M:%S.%f')[:-3]}] Conectando a API: {config_doc.api_name} ({config_doc.api_url})"
        
        # Ejecutar según tipo de análisis
        result = None
        api_start_time = datetime.now()
        
        if doc.tipo_analisis == "Predicción de Seguidores":
            if not doc.fecha_analisis:
                raise Exception("Fecha de análisis requerida para predicción de seguidores")
            doc.log_ejecucion += f"\n[{api_start_time.strftime('%H:%M:%S.%f')[:-3]}] Ejecutando predicción de seguidores..."
            result = doc._ejecutar_prediccion(config_doc)
        elif doc.tipo_analisis == "Clustering":
            if not all([doc.likes, doc.comentarios, doc.compartidos]):
                raise Exception("Likes, comentarios y compartidos requeridos para clustering")
            doc.log_ejecucion += f"\n[{api_start_time.strftime('%H:%M:%S.%f')[:-3]}] Ejecutando clustering..."
            result = doc._ejecutar_clustering(config_doc)
        elif doc.tipo_analisis == "Entrenamiento de Modelo":
            doc.log_ejecucion += f"\n[{api_start_time.strftime('%H:%M:%S.%f')[:-3]}] Ejecutando entrenamiento..."
            result = doc._ejecutar_entrenamiento(config_doc)
        elif doc.tipo_analisis == "Métricas de Modelo":
            doc.log_ejecucion += f"\n[{api_start_time.strftime('%H:%M:%S.%f')[:-3]}] Obteniendo métricas..."
            result = doc._obtener_metricas(config_doc)
        else:
            raise Exception(f"Tipo de análisis no soportado: {doc.tipo_analisis}")
        
        api_end_time = datetime.now()
        api_duration = (api_end_time - api_start_time).total_seconds()
        doc.log_ejecucion += f"\n[{api_end_time.strftime('%H:%M:%S.%f')[:-3]}] API respondió en {api_duration:.2f}s"
        
        # Procesar resultados
        if result:
            process_start_time = datetime.now()
            doc._procesar_resultados(result)
            process_end_time = datetime.now()
            process_duration = (process_end_time - process_start_time).total_seconds()
            
            doc.estado = "Completado"
            total_duration = (process_end_time - start_time).total_seconds()
            doc.log_ejecucion += f"\n[{process_end_time.strftime('%H:%M:%S.%f')[:-3]}] Resultados procesados en {process_duration:.2f}s"
            doc.log_ejecucion += f"\n[{process_end_time.strftime('%H:%M:%S.%f')[:-3]}] ✅ Análisis completado en {total_duration:.2f}s total"
        else:
            raise Exception("La API no devolvió resultados válidos")
        
        return {"success": True, "result": result}
        
    except Exception as e:
        error_time = datetime.now()
        error_duration = (error_time - start_time).total_seconds()
        error_msg = str(e)
        doc.estado = "Error"
        doc.error_message = error_msg
        doc.log_ejecucion += f"\n[{error_time.strftime('%H:%M:%S.%f')[:-3]}] ❌ Error después de {error_duration:.2f}s: {error_msg}"
        frappe.log_error(f"Error en análisis {doc.name}: {error_msg}", "Social Media Analytics")
        return {"success": False, "error": error_msg}
    
    finally:
        try:
            doc.save()
            frappe.db.commit()
        except Exception as save_error:
            frappe.log_error(f"Error guardando documento después del análisis: {str(save_error)}", "Social Media Analytics")


@frappe.whitelist()
def get_analisis_status(docname):
    """Obtener el estado actual del análisis"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", docname)
        return {
            "estado": doc.estado,
            "error_message": doc.error_message,
            "log_ejecucion": doc.log_ejecucion
        }
    except Exception as e:
        return {"error": str(e)}
