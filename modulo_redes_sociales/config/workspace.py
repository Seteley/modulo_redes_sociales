import frappe
from frappe import _


def get_data():
    """Configuración del workspace de Social Media Analytics"""
    return {
        "label": _("Social Media Analytics"),
        "icon": "fa fa-share-alt-square",
        "color": "#3498db",
        "shortcuts": [
            {
                "type": "doctype",
                "name": "API Configuration",
                "label": _("🔧 Configurar API"),
                "format": _("{} Configuraciones"),
                "description": _("Configurar conexión con la API externa de ML"),
                "color": "#e74c3c",
                "icon": "fa fa-cog"
            },
            {
                "type": "doctype",
                "name": "Analisis Redes Sociales", 
                "label": _("📊 Mis Análisis"),
                "format": _("{} Análisis"),
                "description": _("Ver historial de análisis realizados"),
                "color": "#27ae60",
                "icon": "fa fa-list"
            },
            {
                "type": "doctype",
                "name": "Analisis Redes Sociales",
                "doc_view": "New",
                "label": _("➕ Análisis Nuevo"),
                "format": _("Crear Análisis"),
                "description": _("Crear nuevo análisis de predicción o clustering"),
                "color": "#f39c12",
                "icon": "fa fa-plus-circle"
            },
            {
                "type": "page",
                "name": "dashboard",
                "label": _("📈 Dashboard"),
                "format": _("Dashboard"),
                "description": _("Métricas en tiempo real y visualizaciones"),
                "color": "#9b59b6",
                "icon": "fa fa-dashboard"
            }
        ],
        "charts": [],
        "cards": [
            {
                "name": "Estado API",
                "label": _("Estado de la API"),
                "color": "#2ecc71"
            }
        ]
    }
