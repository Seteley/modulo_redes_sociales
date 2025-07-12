# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from datetime import datetime, timedelta


class AnalisisRedesSociales(Document):
    def validate(self):
        """Validar los parámetros del análisis"""
        if self.tipo_analisis == "Predicción de Seguidores":
            if not self.dias_prediccion:
                self.dias_prediccion = 30
            if not self.fecha_prediccion:
                self.fecha_prediccion = datetime.now().date() + timedelta(days=self.dias_prediccion)
        
        elif self.tipo_analisis == "Clustering":
            if not all([self.likes, self.comentarios, self.compartidos]):
                frappe.throw("Para clustering se requieren likes, comentarios y compartidos")

    def before_save(self):
        """Ejecutar antes de guardar"""
        if self.is_new() and self.estado == "Pendiente":
            # Auto-ejecutar el análisis al guardar
            frappe.enqueue(
                method=self.ejecutar_analisis,
                queue='default',
                timeout=300,
                is_async=True
            )

    def ejecutar_analisis(self):
        """Ejecutar el análisis según el tipo seleccionado"""
        try:
            self.estado = "Ejecutando"
            self.save()
            frappe.db.commit()

            # Obtener configuración de API
            api_config = frappe.get_value("API Configuration", 
                                        {"enabled": 1}, 
                                        ["name"], as_dict=True)
            
            if not api_config:
                raise Exception("No hay configuración de API habilitada")
            
            config_doc = frappe.get_doc("API Configuration", api_config.name)
            
            # Ejecutar según tipo de análisis
            if self.tipo_analisis == "Predicción de Seguidores":
                result = self._ejecutar_prediccion(config_doc)
            elif self.tipo_analisis == "Clustering":
                result = self._ejecutar_clustering(config_doc)
            elif self.tipo_analisis == "Entrenamiento de Modelo":
                result = self._ejecutar_entrenamiento(config_doc)
            elif self.tipo_analisis == "Métricas de Modelo":
                result = self._obtener_metricas(config_doc)
            else:
                raise Exception(f"Tipo de análisis no soportado: {self.tipo_analisis}")
            
            # Guardar resultados
            self._procesar_resultados(result)
            self.estado = "Completado"
            self.log_ejecucion = f"Análisis completado exitosamente en {datetime.now()}"
            
        except Exception as e:
            self.estado = "Error"
            self.error_message = str(e)
            self.log_ejecucion = f"Error en análisis: {str(e)} - {datetime.now()}"
            frappe.log_error(f"Error en análisis: {str(e)}", "Social Media Analytics")
        
        finally:
            self.save()
            frappe.db.commit()

    def _ejecutar_prediccion(self, config_doc):
        """Ejecutar predicción de seguidores"""
        params = {}
        if self.fecha_prediccion:
            params['fecha'] = str(self.fecha_prediccion)
        if self.dias_prediccion:
            params['dias'] = self.dias_prediccion
        
        endpoint = f"regression/predict/{self.usuario_red_social}"
        return config_doc.make_api_request(endpoint, params=params)

    def _ejecutar_clustering(self, config_doc):
        """Ejecutar clustering"""
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
        if self.tipo_analisis == "Predicción de Seguidores":
            if "prediction" in result:
                self.prediccion_seguidores = result["prediction"]
            if "confidence" in result:
                self.confianza = result["confidence"]
            if "model_id" in result:
                self.modelo_usado = result["model_id"]

        elif self.tipo_analisis == "Clustering":
            if "cluster" in result:
                self.cluster_asignado = result["cluster"]
            if "cluster_name" in result:
                self.cluster_nombre = result["cluster_name"]

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

    @frappe.whitelist()
    def reejecutar_analisis(self):
        """Re-ejecutar el análisis"""
        self.estado = "Pendiente"
        self.error_message = ""
        self.save()
        
        frappe.enqueue(
            method=self.ejecutar_analisis,
            queue='default',
            timeout=300,
            is_async=True
        )
        
        frappe.msgprint("Análisis en cola para re-ejecución")

    @frappe.whitelist()
    def obtener_publicaciones(self):
        """Obtener publicaciones del usuario desde la API"""
        try:
            api_config = frappe.get_value("API Configuration", 
                                        {"enabled": 1}, 
                                        ["name"], as_dict=True)
            
            if not api_config:
                frappe.throw("No hay configuración de API habilitada")
            
            config_doc = frappe.get_doc("API Configuration", api_config.name)
            endpoint = f"crud/publicaciones/{self.usuario_red_social}"
            
            result = config_doc.make_api_request(endpoint)
            return result
            
        except Exception as e:
            frappe.throw(f"Error al obtener publicaciones: {str(e)}")

    @frappe.whitelist()
    def obtener_metricas_usuario(self):
        """Obtener métricas del usuario desde la API"""
        try:
            api_config = frappe.get_value("API Configuration", 
                                        {"enabled": 1}, 
                                        ["name"], as_dict=True)
            
            if not api_config:
                frappe.throw("No hay configuración de API habilitada")
            
            config_doc = frappe.get_doc("API Configuration", api_config.name)
            endpoint = f"crud/metricas/{self.usuario_red_social}"
            
            result = config_doc.make_api_request(endpoint)
            return result
            
        except Exception as e:
            frappe.throw(f"Error al obtener métricas: {str(e)}")


@frappe.whitelist()
def crear_analisis_rapido(tipo_analisis, usuario_red_social, **kwargs):
    """Crear un análisis rápido"""
    doc = frappe.new_doc("Analisis Redes Sociales")
    doc.titulo = f"Análisis {tipo_analisis} - {usuario_red_social}"
    doc.tipo_analisis = tipo_analisis
    doc.usuario_red_social = usuario_red_social
    
    # Asignar parámetros adicionales
    for key, value in kwargs.items():
        if hasattr(doc, key):
            setattr(doc, key, value)
    
    doc.save()
    return doc
