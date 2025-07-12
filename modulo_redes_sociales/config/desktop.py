import frappe
from frappe import _

def get_data():
    """Configuración del módulo para el escritorio"""
    return [
        {
            "module_name": "Modulo Redes Sociales",
            "color": "#3498db",
            "icon": "fa fa-chart-line",
            "type": "module",
            "label": _("Modulo Redes Sociales"),
            "description": _("Integración con API de Social Media Analytics")
        }
    ]
