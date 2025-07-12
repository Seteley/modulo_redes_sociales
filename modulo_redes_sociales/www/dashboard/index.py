import frappe


def get_context(context):
    """Contexto para la página del dashboard"""
    context.title = "Dashboard de Redes Sociales"
    
    # Obtener análisis recientes
    context.analisis_recientes = frappe.get_all(
        "Analisis Redes Sociales",
        fields=["name", "titulo", "tipo_analisis", "estado", "fecha_creacion", "usuario_red_social"],
        order_by="creation desc",
        limit=10
    )
    
    # Obtener configuración de API
    context.api_config = frappe.get_value("API Configuration", 
                                        {"enabled": 1}, 
                                        ["name", "api_name", "connection_status"], 
                                        as_dict=True)
    
    # Estadísticas generales
    context.stats = {
        "total_analisis": frappe.db.count("Analisis Redes Sociales"),
        "analisis_completados": frappe.db.count("Analisis Redes Sociales", {"estado": "Completado"}),
        "analisis_error": frappe.db.count("Analisis Redes Sociales", {"estado": "Error"}),
        "analisis_pendientes": frappe.db.count("Analisis Redes Sociales", {"estado": "Pendiente"})
    }
    
    return context
