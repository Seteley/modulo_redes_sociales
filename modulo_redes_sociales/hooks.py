app_name = "modulo_redes_sociales"
app_title = "Modulo Redes Sociales"
app_publisher = "G7"
app_description = "Módulo para hacer consultas a un modelo de ML relacionado al número de seguidores de la empresa en redes sociales."
app_email = "tejedasergio2004@gmail.com"
app_license = "mit"

app_include_css = "/assets/modulo_redes_sociales/css/modulo_redes_sociales.css"
app_include_js = "/assets/modulo_redes_sociales/js/modulo_redes_sociales.js"

# Agregar esta línea
app_logo_url = "/assets/modulo_redes_sociales/images/logo.png"

# Esto muestra el módulo en el escritorio
app_include_js = "/assets/modulo_redes_sociales/js/modulo_redes_sociales.js"

# Agrega tu página
website_route_rules = [
    {"from_route": "/", "to_route": "modulo_redes_sociales"}
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
    {
        "name": "modulo_redes_sociales",
        "logo": "/assets/modulo_redes_sociales/logo.png",
        "title": "Modulo Redes Sociales",
        "route": "/modulo_redes_sociales"
        # "has_permission": "modulo_redes_sociales.api.permission.has_app_permission"  # Descomenta si tienes esta función
    }
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/modulo_redes_sociales/css/modulo_redes_sociales.css"
# app_include_js = "/assets/modulo_redes_sociales/js/modulo_redes_sociales.js"

# include js, css files in header of web template
# web_include_css = "/assets/modulo_redes_sociales/css/modulo_redes_sociales.css"
# web_include_js = "/assets/modulo_redes_sociales/js/modulo_redes_sociales.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "modulo_redes_sociales/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "modulo_redes_sociales/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "modulo_redes_sociales.utils.jinja_methods",
# 	"filters": "modulo_redes_sociales.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "modulo_redes_sociales.install.before_install"
# after_install = "modulo_redes_sociales.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "modulo_redes_sociales.uninstall.before_uninstall"
# after_uninstall = "modulo_redes_sociales.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "modulo_redes_sociales.utils.before_app_install"
# after_app_install = "modulo_redes_sociales.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "modulo_redes_sociales.utils.before_app_uninstall"
# after_app_uninstall = "modulo_redes_sociales.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "modulo_redes_sociales.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"modulo_redes_sociales.tasks.all"
# 	],
# 	"daily": [
# 		"modulo_redes_sociales.tasks.daily"
# 	],
# 	"hourly": [
# 		"modulo_redes_sociales.tasks.hourly"
# 	],
# 	"weekly": [
# 		"modulo_redes_sociales.tasks.weekly"
# 	],
# 	"monthly": [
# 		"modulo_redes_sociales.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "modulo_redes_sociales.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "modulo_redes_sociales.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "modulo_redes_sociales.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["modulo_redes_sociales.utils.before_request"]
# after_request = ["modulo_redes_sociales.utils.after_request"]

# Job Events
# ----------
# before_job = ["modulo_redes_sociales.utils.before_job"]
# after_job = ["modulo_redes_sociales.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"modulo_redes_sociales.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

