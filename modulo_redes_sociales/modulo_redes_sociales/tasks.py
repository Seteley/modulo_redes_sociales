# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime, add_to_date


def process_pending_analysis():
    """Procesar análisis pendientes en background"""
    try:
        # Obtener análisis pendientes
        pending_analysis = frappe.get_all(
            "Analisis Redes Sociales",
            filters={"estado": "Pendiente"},
            fields=["name"],
            limit=5  # Procesar máximo 5 a la vez
        )
        
        for analysis in pending_analysis:
            try:
                doc = frappe.get_doc("Analisis Redes Sociales", analysis.name)
                doc.ejecutar_analisis()
                frappe.db.commit()
            except Exception as e:
                frappe.log_error(f"Error procesando análisis {analysis.name}: {str(e)}", 
                               "Background Analysis Processing")
                
                # Marcar como error si falla
                doc = frappe.get_doc("Analisis Redes Sociales", analysis.name)
                doc.estado = "Error"
                doc.error_message = str(e)
                doc.save()
                frappe.db.commit()
                
    except Exception as e:
        frappe.log_error(f"Error en proceso background: {str(e)}", 
                       "Background Process Error")


def cleanup_old_tokens():
    """Limpiar tokens expirados de configuraciones de API"""
    try:
        # Obtener configuraciones con tokens expirados
        expired_configs = frappe.get_all(
            "API Configuration",
            filters={
                "token_expiry": ["<", now_datetime()],
                "access_token": ["!=", ""]
            },
            fields=["name"]
        )
        
        for config in expired_configs:
            doc = frappe.get_doc("API Configuration", config.name)
            doc.access_token = ""
            doc.token_expiry = None
            doc.connection_status = "No probado"
            doc.save()
            
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Error limpiando tokens: {str(e)}", 
                       "Token Cleanup Error")


def generate_analysis_summary():
    """Generar resumen diario de análisis"""
    try:
        # Obtener estadísticas del día
        from frappe.utils import today
        
        today_stats = frappe.db.sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN estado = 'Completado' THEN 1 ELSE 0 END) as completados,
                SUM(CASE WHEN estado = 'Error' THEN 1 ELSE 0 END) as errores,
                tipo_analisis,
                COUNT(*) as count_por_tipo
            FROM `tabAnalisis Redes Sociales`
            WHERE DATE(creation) = %s
            GROUP BY tipo_analisis
        """, (today(),), as_dict=True)
        
        if today_stats:
            # Crear log de resumen diario
            summary = {
                "fecha": today(),
                "estadisticas": today_stats,
                "timestamp": now_datetime()
            }
            
            frappe.log_error(f"Resumen diario de análisis: {summary}", 
                           "Daily Analysis Summary")
            
    except Exception as e:
        frappe.log_error(f"Error generando resumen: {str(e)}", 
                       "Summary Generation Error")
