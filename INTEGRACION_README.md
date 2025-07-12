# 🚀 Integración Social Media Analytics API - ERPNext

Esta es la integración completa de la API de Social Media Analytics con ERPNext, implementada dentro del módulo `modulo_redes_sociales`.

## 📋 Componentes Integrados

### 🔧 DocTypes Principales

#### 1. **API Configuration**
- **Ubicación**: `apps/modulo_redes_sociales/modulo_redes_sociales/modulo_redes_sociales/doctype/api_configuration/`
- **Función**: Gestionar la configuración y autenticación con la API externa
- **Características**:
  - Configuración de URL, credenciales y timeouts
  - Gestión automática de tokens JWT
  - Prueba de conexión integrada
  - Sistema de reintentos automáticos

#### 2. **Analisis Redes Sociales**
- **Ubicación**: `apps/modulo_redes_sociales/modulo_redes_sociales/modulo_redes_sociales/doctype/analisis_redes_sociales/`
- **Función**: Gestionar análisis predictivos y de clustering
- **Tipos de Análisis**:
  - 📈 **Predicción de Seguidores**: Predecir crecimiento futuro
  - 🎯 **Clustering**: Clasificar publicaciones por engagement
  - 🤖 **Entrenamiento de Modelo**: Entrenar modelos ML personalizados
  - 📊 **Métricas de Modelo**: Obtener estadísticas de rendimiento

### 🌐 Dashboard Web
- **URL**: `http://erpnext.localhost/dashboard`
- **Archivo**: `apps/modulo_redes_sociales/modulo_redes_sociales/www/dashboard/`
- **Características**:
  - Vista general de estadísticas
  - Creación rápida de análisis
  - Monitoreo de estado de API
  - Auto-refresh cada 30 segundos

### 🔗 API Endpoints
- **Archivo**: `apps/modulo_redes_sociales/modulo_redes_sociales/modulo_redes_sociales/api.py`
- **Endpoints disponibles**:
  - `get_dashboard_stats()`: Estadísticas del dashboard
  - `test_api_connection()`: Probar conexión con API
  - `create_quick_analysis()`: Crear análisis rápido
  - `get_user_metrics()`: Métricas de usuario
  - `export_analysis_results()`: Exportar resultados

## 🚀 Configuración e Instalación

### 1. **Migrar Base de Datos**
```bash
cd /home/marzabe/final_analitica/erp-dev
bench --site erpnext.localhost migrate
```

### 2. **Inicializar Datos**
```bash
cd /home/marzabe/final_analitica/erp-dev
python init_social_media_module.py
```

### 3. **Verificar Instalación**
- Acceder a ERPNext: `http://erpnext.localhost`
- Buscar el módulo "Modulo Redes Sociales"
- Verificar que aparezcan los DocTypes:
  - API Configuration
  - Analisis Redes Sociales

## 📖 Uso del Sistema

### 🔧 Configuración Inicial

1. **Configurar API**:
   - Ir a "API Configuration"
   - Crear nueva configuración:
     - API URL: `http://localhost:8000`
     - Usuario: `admin`
     - Contraseña: `password123`
   - Hacer clic en "Probar Conexión"

2. **Verificar Dashboard**:
   - Acceder a `http://erpnext.localhost/dashboard`
   - Verificar estado de la API
   - Ver estadísticas iniciales

### 📊 Crear Análisis

#### Método 1: Dashboard Web
- Ir a `http://erpnext.localhost/dashboard`
- Usar botones de "Acciones Rápidas"
- Completar formulario según tipo de análisis

#### Método 2: ERPNext Interface
- Ir a "Analisis Redes Sociales" > "Nuevo"
- Completar campos requeridos
- Guardar (se ejecuta automáticamente)

### 📈 Tipos de Análisis Disponibles

#### 1. **Predicción de Seguidores**
```
Parámetros:
- Usuario de Red Social: Ej. "Interbank"
- Días para Predicción: 30 (por defecto)

Resultado:
- Número predicho de seguidores
- Nivel de confianza del modelo
```

#### 2. **Clustering**
```
Parámetros:
- Usuario: Ej. "BCPComunica"
- Likes: 1500
- Comentarios: 89
- Compartidos: 234

Resultado:
- Cluster asignado (0, 1, 2...)
- Nombre del cluster ("Alto Engagement", etc.)
```

#### 3. **Entrenamiento de Modelo**
```
Parámetros:
- Usuario: Ej. "BBVA_Peru"

Resultado:
- ID del modelo entrenado
- Métricas: R², MAE, RMSE
```

#### 4. **Métricas de Modelo**
```
Parámetros:
- Usuario: Ej. "MiBanco"

Resultado:
- R² (coeficiente de determinación)
- MAE (Error Absoluto Medio)
- RMSE (Raíz del Error Cuadrático Medio)
```

## 🔄 Flujo de Trabajo Típico

1. **Configurar API** (una vez)
2. **Entrenar modelo** para un usuario específico
3. **Verificar métricas** del modelo entrenado
4. **Hacer predicciones** de seguidores
5. **Analizar contenido** con clustering
6. **Exportar resultados** para reportes

## 🛠️ Características Técnicas

### 🔐 Seguridad
- Autenticación JWT automática
- Renovación automática de tokens
- Gestión segura de credenciales

### ⚡ Performance
- Ejecución asíncrona de análisis
- Sistema de reintentos automáticos
- Cache de tokens y conexiones

### 📊 Monitoreo
- Logs detallados de cada análisis
- Estados de ejecución en tiempo real
- Alertas de errores y fallos

### 🔄 Tareas Programadas
- Procesamiento de análisis pendientes cada 5 minutos
- Limpieza automática de tokens expirados
- Generación de resúmenes diarios

## 📁 Estructura de Archivos

```
apps/modulo_redes_sociales/
├── modulo_redes_sociales/
│   ├── modulo_redes_sociales/
│   │   ├── doctype/
│   │   │   ├── api_configuration/
│   │   │   │   ├── api_configuration.json
│   │   │   │   ├── api_configuration.py
│   │   │   │   └── __init__.py
│   │   │   └── analisis_redes_sociales/
│   │   │       ├── analisis_redes_sociales.json
│   │   │       ├── analisis_redes_sociales.py
│   │   │       └── __init__.py
│   │   ├── api.py
│   │   ├── tasks.py
│   │   └── __init__.py
│   ├── www/
│   │   └── dashboard/
│   │       ├── index.py
│   │       └── index.html
│   ├── public/
│   │   ├── css/
│   │   │   └── dashboard.css
│   │   └── js/
│   │       └── dashboard.js
│   ├── config/
│   │   ├── desktop.py
│   │   └── modulo_redes_sociales.py
│   └── hooks.py
├── API_DOCUMENTACION_COMPLETA.md
└── README.md (este archivo)
```

## 🧪 Testing y Debugging

### Verificar Estado del Sistema
```bash
# Verificar ERPNext
curl -I http://erpnext.localhost

# Verificar API Externa (si está disponible)
curl -I http://localhost:8000

# Ver logs de ERPNext
tail -f /home/marzabe/final_analitica/erp-dev/logs/web.log
```

### Debugging Common Issues

1. **API no responde**:
   - Verificar que la API externa esté ejecutándose en puerto 8000
   - Revisar configuración de URL en "API Configuration"

2. **Análisis se queda en "Pendiente"**:
   - Verificar logs de error en ERPNext
   - Comprobar credenciales en "API Configuration"

3. **Dashboard no carga**:
   - Verificar que `bench` esté ejecutándose
   - Reiniciar servicios: `bench --site erpnext.localhost restart`

## 📞 Soporte

Para reportar problemas o solicitar nuevas características:

1. Revisar logs en `/home/marzabe/final_analitica/erp-dev/logs/`
2. Verificar configuración de API
3. Comprobar estado de servicios

---

**Este módulo proporciona una integración completa entre ERPNext y la API de Social Media Analytics, permitiendo análisis predictivos y de machine learning directamente desde la interfaz de ERPNext.** 🚀
