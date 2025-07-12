# Copyright (c) 2024, Tu Empresa and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_data():
    """Datos para el escritorio del módulo con navegación intuitiva"""
    return [
        {
            "module_name": "Modulo Redes Sociales",
            "color": "#3498db",
            "icon": "fa fa-share-alt-square",
            "type": "module",
            "label": _("Social Media Analytics"),
            "description": _("Análisis predictivo de redes sociales con Machine Learning"),
            "shortcuts": [
                {
                    "type": "doctype",
                    "name": "API Configuration",
                    "label": _("🔧 Configurar API"),
                    "description": _("Configurar conexión con la API externa"),
                    "color": "#e74c3c"
                },
                {
                    "type": "doctype", 
                    "name": "Analisis Redes Sociales",
                    "label": _("📊 Ver Análisis"),
                    "description": _("Lista de análisis realizados"),
                    "color": "#27ae60"
                },
                {
                    "type": "doctype",
                    "name": "Analisis Redes Sociales", 
                    "label": _("➕ Nuevo Análisis"),
                    "description": _("Crear análisis de redes sociales"),
                    "color": "#f39c12",
                    "link": "/app/analisis-redes-sociales/new"
                },
                {
                    "type": "page",
                    "name": "dashboard",
                    "label": _("📈 Dashboard"),
                    "description": _("Ver métricas y resultados"),
                    "color": "#9b59b6"
                }
            ]
        }
    ]
