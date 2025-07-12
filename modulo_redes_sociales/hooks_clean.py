app_name = "modulo_redes_sociales"
app_title = "Modulo Redes Sociales"
app_publisher = "G7"
app_description = "Módulo para integración con API de Social Media Analytics"
app_email = "admin@empresa.com"
app_license = "mit"
app_version = "1.0.0"

# Apps requeridas
required_apps = ["frappe", "erpnext"]

# Páginas web
website_route_rules = [
    {"from_route": "/dashboard", "to_route": "dashboard"}
]

# CSS y JS para el módulo
app_include_css = "/assets/modulo_redes_sociales/css/dashboard.css"
app_include_js = "/assets/modulo_redes_sociales/js/dashboard.js"

# Fixtures - vacío para evitar problemas
fixtures = []
