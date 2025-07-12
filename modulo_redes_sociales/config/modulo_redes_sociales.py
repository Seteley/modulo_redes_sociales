import frappe
from frappe import _

def get_data():
    """Configuración del módulo Social Media Analytics"""
    return {
        "heatmap": False,
        "disable_heatmap": True,
        "shortcuts": [
            {
                "label": _("API Configuration"),
                "doc_view": "List",
                "type": "DocType",
                "description": _("Configurar API externa"),
                "name": "API Configuration"
            },
            {
                "label": _("Analisis Redes Sociales"),
                "doc_view": "List", 
                "type": "DocType",
                "description": _("Gestionar análisis de redes sociales"),
                "name": "Analisis Redes Sociales"
            },
            {
                "label": _("Nuevo Análisis"),
                "doc_view": "New",
                "type": "DocType",
                "description": _("Crear nuevo análisis"),
                "name": "Analisis Redes Sociales"
            },
            {
                "label": _("Dashboard"),
                "url": "/dashboard",
                "type": "URL",
                "description": _("Ver dashboard de resultados")
            }
        ]
    }
            {
                "label": _("Configuración"),
                "items": [
                    {
                        "type": "DocType",
                        "name": "API Configuration",
                        "label": _("Configuración de API"),
                        "description": _("Configurar conexión con la API de Social Media Analytics")
                    }
                ]
            },
            {
                "label": _("Análisis"),
                "items": [
                    {
                        "type": "DocType",
                        "name": "Analisis Redes Sociales",
                        "label": _("Análisis de Redes Sociales"),
                        "description": _("Gestionar análisis predictivos y clustering")
                    }
                ]
            },
            {
                "label": _("Reportes y Dashboards"),
                "items": [
                    {
                        "type": "URL",
                        "url": "/dashboard",
                        "label": _("Dashboard Principal"),
                        "description": _("Vista principal con métricas y análisis")
                    }
                ]
            }
        ]
    }
