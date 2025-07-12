# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


@frappe.whitelist()
def get_dashboard_stats() -> Dict[str, Any]:
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
def get_recent_analysis(limit: int = 10) -> List[Dict[str, Any]]:
    """Obtener análisis recientes"""
    return frappe.get_all(
        "Analisis Redes Sociales",
        fields=["name", "titulo", "tipo_analisis", "estado", "fecha_creacion", 
               "usuario_red_social", "prediccion_seguidores", "cluster_asignado"],
        order_by="creation desc",
        limit=limit
    )


@frappe.whitelist()
def test_api_connection() -> Dict[str, Any]:
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
def create_quick_analysis(tipo_analisis: str, usuario_red_social: str, **kwargs) -> Dict[str, Any]:
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
def get_user_metrics(usuario: str) -> Dict[str, Any]:
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
def get_user_posts(usuario: str) -> Dict[str, Any]:
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
def get_model_comparison(usuario1: str, usuario2: str) -> Dict[str, Any]:
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
def export_analysis_results(analysis_name: str) -> Dict[str, Any]:
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


@frappe.whitelist()
def ejecutar_analisis(analisis_id: str) -> Dict[str, Any]:
    """Ejecutar análisis de redes sociales"""
    try:
        if not analisis_id:
            return {"success": False, "error": "ID de análisis requerido"}
        
        # Obtener el documento del análisis
        doc = frappe.get_doc("Analisis Redes Sociales", analisis_id)
        
        # Validar que el documento existe y está en estado válido
        if not doc:
            return {"success": False, "error": "Análisis no encontrado"}
        
        if doc.estado == "Completado":
            return {"success": False, "error": "El análisis ya está completado"}
        
        if doc.estado == "Ejecutando":
            return {"success": False, "error": "El análisis ya se está ejecutando"}
        
        # Validar que tenga configuración de API
        if not doc.api_configuration:
            return {"success": False, "error": "No hay configuración de API seleccionada"}
        
        # Validar campos requeridos según el tipo de análisis
        if doc.tipo_analisis == "Predicción de Seguidores":
            if not doc.fecha_analisis:
                return {"success": False, "error": "Fecha de análisis requerida para predicción de seguidores"}
        
        elif doc.tipo_analisis == "Clustering":
            # El clustering ahora solo requiere usuario y configuración API
            # No necesita parámetros adicionales ya que usa el modelo pkl guardado
            pass
        
        # Cambiar estado a ejecutando
        doc.estado = "Ejecutando"
        doc.save()
        frappe.db.commit()
        
        # Ejecutar análisis en segundo plano
        frappe.enqueue(
            method=_ejecutar_analisis_background,
            queue='default',
            timeout=300,
            is_async=True,
            analisis_id=analisis_id
        )
        
        return {"success": True, "message": "Análisis iniciado correctamente"}
        
    except Exception as e:
        frappe.log_error(f"Error al ejecutar análisis: {str(e)}")
        return {"success": False, "error": f"Error inesperado: {str(e)}"}


def _ejecutar_analisis_background(analisis_id: str) -> None:
    """Ejecutar análisis en segundo plano"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", analisis_id)
        
        # Ejecutar el método del documento
        result = doc.ejecutar_analisis()
        
        # Actualizar estado según resultado
        if result and result.get("success"):
            doc.estado = "Completado"
            if "prediccion" in result:
                doc.prediccion_seguidores = result["prediccion"]
            if "cluster" in result:
                doc.cluster_asignado = result["cluster"]
                doc.cluster_nombre = result.get("cluster_nombre", "")
            if "metricas" in result:
                doc.metricas_modelo = json.dumps(result["metricas"], indent=2)
        else:
            doc.estado = "Error"
            doc.error_message = result.get("error", "Error desconocido") if result else "Error en la ejecución"
        
        doc.save()
        frappe.db.commit()
        
    except Exception as e:
        try:
            doc = frappe.get_doc("Analisis Redes Sociales", analisis_id)
            doc.estado = "Error"
            doc.error_message = str(e)
            doc.save()
            frappe.db.commit()
        except:
            pass
        frappe.log_error(f"Error en análisis background: {str(e)}")


@frappe.whitelist()
def get_analisis_status(analisis_id: str) -> Dict[str, Any]:
    """Obtener estado actual del análisis"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", analisis_id)
        return {
            "success": True,
            "estado": doc.estado,
            "error_message": doc.error_message or "",
            "prediccion_seguidores": doc.prediccion_seguidores,
            "cluster_asignado": doc.cluster_asignado,
            "cluster_nombre": doc.cluster_nombre
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def ejecutar_analisis_directo(analisis_id: str) -> Dict[str, Any]:
    """Ejecutar análisis directamente sin background queue (para desarrollo)"""
    try:
        start_time = datetime.now()
        
        doc = frappe.get_doc("Analisis Redes Sociales", analisis_id)
        doc.estado = "Ejecutando"
        doc.log_ejecucion = f"[{start_time.strftime('%H:%M:%S.%f')[:-3]}] 🚀 Ejecución directa iniciada..."
        doc.save()
        frappe.db.commit()
        
        # Verificar configuración de API
        if not doc.api_configuration:
            raise Exception("No hay configuración de API seleccionada")
        
        config_doc = frappe.get_doc("API Configuration", doc.api_configuration)
        if not config_doc.enabled:
            raise Exception(f"La configuración de API '{doc.api_configuration}' no está habilitada")
        
        connect_time = datetime.now()
        doc.log_ejecucion += f"\n[{connect_time.strftime('%H:%M:%S.%f')[:-3]}] Conectando a: {config_doc.api_url}"
        
        # Ejecutar análisis según tipo
        api_start = datetime.now()
        result = None
        
        if doc.tipo_analisis == "Predicción de Seguidores":
            result = doc._ejecutar_prediccion_dev()
        elif doc.tipo_analisis == "Clustering":
            result = doc._ejecutar_clustering_dev()
        elif doc.tipo_analisis == "Entrenamiento de Modelo":
            result = doc._ejecutar_entrenamiento(config_doc)
        elif doc.tipo_analisis == "Métricas de Modelo":
            result = doc._obtener_metricas(config_doc)
        
        api_duration = (datetime.now() - api_start).total_seconds()
        doc.log_ejecucion += f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] API completada en {api_duration:.2f}s"
        
        # Los métodos _dev ya procesan sus propios resultados
        if result and result.get("success"):
            total_duration = (datetime.now() - start_time).total_seconds()
            doc.log_ejecucion += f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ✅ Completado en {total_duration:.2f}s total"
            doc.save()
            frappe.db.commit()
            
            return {
                "success": True,
                "message": f"Análisis completado en {total_duration:.2f} segundos",
                "duration": total_duration,
                "result": result.get("result", {})
            }
        else:
            raise Exception("API no devolvió resultados válidos")
            
    except Exception as e:
        error_duration = (datetime.now() - start_time).total_seconds()
        doc.estado = "Error"
        doc.error_message = str(e)
        doc.log_ejecucion += f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] ❌ Error en {error_duration:.2f}s: {str(e)}"
        doc.save()
        frappe.db.commit()
        
        return {
            "success": False,
            "message": str(e),
            "duration": error_duration
        }


@frappe.whitelist()
def descargar_clustering_completo(docname: str) -> Dict[str, Any]:
    """Download complete clustering results for an analysis"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", docname)
        
        if doc.tipo_analisis != "Clustering":
            frappe.throw("Este análisis no es de tipo Clustering")
        
        return doc.descargar_resultados_completos()
        
    except Exception as e:
        frappe.throw(f"Error al preparar descarga: {str(e)}")


@frappe.whitelist()
def get_clustering_summary(docname: str) -> Dict[str, Any]:
    """Get clustering summary for display"""
    try:
        doc = frappe.get_doc("Analisis Redes Sociales", docname)
        
        if not doc.resumen_clusters:
            return {"error": "No hay resumen de clusters disponible"}
        
        summary = json.loads(doc.resumen_clusters)
        
        # Add additional formatting for display
        summary["formatted_engagement"] = f"{summary.get('avg_engagement_rate', 0):.2%}"
        summary["formatted_likes"] = f"{summary.get('total_likes', 0):,}"
        summary["formatted_views"] = f"{summary.get('total_views', 0):,}"
        
        return {
            "success": True,
            "summary": summary,
            "estado": doc.estado,
            "fecha_analisis": str(doc.fecha_analisis) if doc.fecha_analisis else None
        }
        
    except Exception as e:
        return {"error": str(e)}
