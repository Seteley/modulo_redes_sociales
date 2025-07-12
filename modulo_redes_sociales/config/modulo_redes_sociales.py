# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_data():
    """Configuración para el workspace del módulo"""
    return {
        "heatmap": True,
        "heatmap_message": _("Este es el módulo de Social Media Analytics para ERPNext."),
        "disable_heatmap": False,
        "charts": [
            {
                "label": _("Análisis por Mes"),
                "chart_name": _("Análisis por Mes"),
                "chart_type": "Count",
                "document_type": "Analisis Redes Sociales",
                "based_on": "fecha_creacion",
                "timespan": "Last Year",
                "time_interval": "Monthly",
                "filters_config": {
                    "estado": "Completado"
                }
            }
        ],
        "shortcuts": [
            {
                "label": _("API Configuration"),
                "doc_view": "List",
                "type": "DocType",
                "description": _("Configurar conexión con API externa"),
                "name": "API Configuration"
            },
            {
                "label": _("Nuevo Análisis"),
                "doc_view": "New",
                "type": "DocType", 
                "description": _("Crear nuevo análisis de redes sociales"),
                "name": "Analisis Redes Sociales"
            },
            {
                "label": _("Dashboard"),
                "url": "/dashboard",
                "type": "URL",
                "description": _("Ver dashboard de analytics")
            }
        ],
        "cards": [
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
