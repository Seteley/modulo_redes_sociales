# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json


@frappe.whitelist()
def get_dashboard_stats():
    """Obtener estadísticas para el dashboard"""
    stats = {
        "total_analisis": frappe.db.count("Analisis Redes Sociales"),
        "analisis_completados": frappe.db.count("Analisis Redes Sociales", {"estado": "Completado"}),
        "analisis_error": frappe.db.count("Analisis Redes Sociales", {"estado": "Error"}),
        "analisis_pendientes": frappe.db.count("Analisis Redes Sociales", {"estado": "Pendiente"}),
        "analisis_ejecutando": frappe.db.count("Analisis Redes Sociales", {"estado": "Ejecutando"})
    }
    
    # Obtener análisis por tipo
    tipos_analisis = frappe.db.sql("""
        SELECT tipo_analisis, COUNT(*) as count
        FROM `tabAnalisis Redes Sociales`
        GROUP BY tipo_analisis
    """, as_dict=True)
    
    stats["por_tipo"] = {item["tipo_analisis"]: item["count"] for item in tipos_analisis}
    
    return stats


@frappe.whitelist()
def get_recent_analysis(limit=10):
    """Obtener análisis recientes"""
    return frappe.get_all(
        "Analisis Redes Sociales",
        fields=["name", "titulo", "tipo_analisis", "estado", "fecha_creacion", 
               "usuario_red_social", "prediccion_seguidores", "cluster_asignado"],
        order_by="creation desc",
        limit=limit
    )


@frappe.whitelist()
def test_api_connection():
    """Probar conexión con la API externa"""
    try:
        # Obtener configuración activa
        config = frappe.get_value("API Configuration", 
                                {"enabled": 1}, 
                                ["name"], as_dict=True)
        
        if not config:
            return {"success": False, "message": "No hay configuración de API habilitada"}
        
        config_doc = frappe.get_doc("API Configuration", config.name)
        result = config_doc.test_api_connection()
        
        return {"success": True, "message": "Conexión exitosa"}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def create_quick_analysis(tipo_analisis, usuario_red_social, **kwargs):
    """Crear un análisis rápido desde el dashboard"""
    try:
        # Crear nuevo documento
        doc = frappe.new_doc("Analisis Redes Sociales")
        doc.titulo = f"Análisis {tipo_analisis} - {usuario_red_social}"
        doc.tipo_analisis = tipo_analisis
        doc.usuario_red_social = usuario_red_social
        
        # Asignar parámetros específicos
        for key, value in kwargs.items():
            if hasattr(doc, key) and value:
                setattr(doc, key, value)
        
        doc.save()
        
        return {
            "success": True, 
            "message": "Análisis creado exitosamente",
            "name": doc.name
        }
        
    except Exception as e:
        frappe.log_error(f"Error al crear análisis rápido: {str(e)}")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_user_metrics(usuario):
    """Obtener métricas de un usuario específico"""
    try:
        # Obtener configuración de API
        config = frappe.get_value("API Configuration", 
                                {"enabled": 1}, 
                                ["name"], as_dict=True)
        
        if not config:
            return {"success": False, "message": "No hay configuración de API habilitada"}
        
        config_doc = frappe.get_doc("API Configuration", config.name)
        
        # Obtener métricas desde la API
        endpoint = f"crud/metricas/{usuario}"
        result = config_doc.make_api_request(endpoint)
        
        return {"success": True, "data": result}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_user_posts(usuario):
    """Obtener publicaciones de un usuario específico"""
    try:
        # Obtener configuración de API
        config = frappe.get_value("API Configuration", 
                                {"enabled": 1}, 
                                ["name"], as_dict=True)
        
        if not config:
            return {"success": False, "message": "No hay configuración de API habilitada"}
        
        config_doc = frappe.get_doc("API Configuration", config.name)
        
        # Obtener publicaciones desde la API
        endpoint = f"crud/publicaciones/{usuario}"
        result = config_doc.make_api_request(endpoint)
        
        return {"success": True, "data": result}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_model_comparison(usuario1, usuario2):
    """Comparar modelos entre dos usuarios"""
    try:
        # Obtener configuración de API
        config = frappe.get_value("API Configuration", 
                                {"enabled": 1}, 
                                ["name"], as_dict=True)
        
        if not config:
            return {"success": False, "message": "No hay configuración de API habilitada"}
        
        config_doc = frappe.get_doc("API Configuration", config.name)
        
        # Obtener métricas de ambos usuarios
        metricas1 = config_doc.make_api_request(f"regression/metrics/{usuario1}")
        metricas2 = config_doc.make_api_request(f"regression/metrics/{usuario2}")
        
        comparison = {
            "usuario1": {
                "nombre": usuario1,
                "metricas": metricas1
            },
            "usuario2": {
                "nombre": usuario2,
                "metricas": metricas2
            }
        }
        
        return {"success": True, "data": comparison}
        
    except Exception as e:
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def export_analysis_results(analysis_name):
    """Exportar resultados de un análisis"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", analysis_name)
        
        export_data = {
            "titulo": doc.titulo,
            "tipo_analisis": doc.tipo_analisis,
            "usuario_red_social": doc.usuario_red_social,
            "estado": doc.estado,
            "fecha_creacion": str(doc.fecha_creacion),
            "prediccion_seguidores": doc.prediccion_seguidores,
            "cluster_asignado": doc.cluster_asignado,
            "cluster_nombre": doc.cluster_nombre,
            "confianza": doc.confianza,
            "metricas_modelo": doc.metricas_modelo
        }
        
        return {"success": True, "data": export_data}
        
    except Exception as e:
        return {"success": False, "message": str(e)}
