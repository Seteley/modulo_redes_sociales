# 🚀 Social Media Analytics API - Documentación Completa

## 📋 Índice
- [Información General](#información-general)
- [Tipo de API](#tipo-de-api)
- [Funcionalidades](#funcionalidades)
- [Stack Tecnológico](#stack-tecnológico)
- [Datos que Maneja](#datos-que-maneja)
- [Casos de Uso](#casos-de-uso)
- [Arquitectura](#arquitectura)
- [Endpoints Principales](#endpoints-principales)
- [Autenticación](#autenticación)
- [Escalabilidad](#escalabilidad)
- [Instalación y Uso](#instalación-y-uso)

---

## 🎯 Información General

**Social Media Analytics API** es una API REST empresarial que proporciona servicios de Machine Learning para análisis predictivo de redes sociales en el sector financiero peruano.

### ✨ Características Destacadas
- 🤖 **Machine Learning as a Service** - Predicciones sin código
- 🏢 **Multi-tenant** - Aislamiento por empresa
- 🔐 **JWT Authentication** - Seguridad empresarial
- 📊 **Analytics-First** - Optimizado para análisis de datos
- 📚 **Auto-documented** - Swagger UI integrado

---

## 🌐 Tipo de API

### **REST API con FastAPI**
```
🔗 Protocolo: HTTP/HTTPS
📊 Formato: JSON
📚 Documentación: OpenAPI 3.0 (Swagger)
🔐 Autenticación: JWT Bearer Token
🎯 Estilo: RESTful
```

### **Endpoints Base**
```
🌐 Servidor: http://localhost:8000
📚 Documentación: http://localhost:8000/docs
🔍 Schema: http://localhost:8000/openapi.json
```

---

## ⚙️ Funcionalidades

### 🤖 **1. Machine Learning Services**

#### 📈 **Regresión Predictiva**
- **Predicción de seguidores** en redes sociales
- **Entrenamiento automático** de modelos personalizados
- **Métricas de rendimiento** (R², MAE, RMSE)
- **Comparación de modelos** entre cuentas
- **Historial de entrenamientos** por empresa

#### 🎯 **Clustering Inteligente**
- **Agrupación de publicaciones** por patrones de engagement
- **Análisis de comportamiento** de audiencia
- **Segmentación automática** de contenido
- **Identificación de clusters** óptimos
- **Visualización de patrones** de datos

### 🔐 **2. Sistema de Autenticación Empresarial**

#### 🏢 **Multi-tenant Architecture**
- **8 empresas financieras** soportadas
- **Control de acceso granular** por empresa
- **Roles diferenciados** (admin, user, viewer)
- **Aislamiento total** de datos entre empresas

#### 👥 **Gestión de Usuarios**
- **Autenticación JWT** con tokens seguros
- **Gestión de sesiones** y renovación
- **Control de usuarios** activos/inactivos
- **Auditoría de accesos** por empresa

### 📊 **3. CRUD de Datos Sociales**

#### 📱 **Gestión de Publicaciones**
- **CRUD completo** de publicaciones
- **Métricas por post** (likes, comentarios, shares)
- **Filtrado avanzado** por empresa y usuario
- **Exportación de datos** para análisis

#### 📈 **Métricas y Reportes**
- **Dashboard de métricas** por cuenta
- **Tendencias temporales** de engagement
- **Comparativas** entre cuentas
- **Reportes automáticos** de rendimiento

---

## 🛠️ Stack Tecnológico

### **Backend Core**
```python
🐍 Lenguaje: Python 3.13
⚡ Framework: FastAPI 0.104+
🌐 Server: Uvicorn (ASGI)
📊 Validación: Pydantic
🔄 Async: AsyncIO support
```

### **Base de Datos**
```sql
🗄️ Engine: DuckDB (Analytics-oriented)
📊 Tipo: Columnar OLAP
🚀 Performance: Optimizado para agregaciones
💾 Storage: Archivo local + memoria
🔍 SQL: Soporte completo ANSI SQL
```

### **Machine Learning**
```python
🤖 Core: scikit-learn
📊 Data: pandas + numpy
🎯 Models: RandomForest, LinearRegression, KMeans
💾 Serialization: pickle
📈 Metrics: sklearn.metrics
```

### **Seguridad y Auth**
```python
🔐 JWT: python-jose[cryptography]
🛡️ Hashing: bcrypt
🔑 Tokens: HS256 algorithm
⏰ Expiry: Configurable TTL
```

### **Dependencias Principales**
```bash
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
duckdb>=0.9.2
scikit-learn>=1.3.2
pandas>=2.1.4
numpy>=1.26.2
python-jose[cryptography]>=3.3.0
bcrypt>=4.1.2
pydantic>=2.5.0
```

---

## 📊 Datos que Maneja

### 🏢 **Empresas Financieras Peruanas**
```
🏦 Banco de Crédito del Perú (BCP) - @BCPComunica
🏦 Interbank - @Interbank  
🏦 BBVA Perú - @bbva_peru
🏦 Scotiabank Perú - @ScotiabankPE
🏦 Banco de la Nación - @BancodelaNacion
🏦 BCRP - @bcrpoficial
🏦 Banco Pichincha - @BancoPichincha
🏦 Banbif - @BanBif
```

### 📱 **Estructura de Datos - Publicaciones**
```json
{
  "id_publicacion": "integer",
  "id_usuario": "integer", 
  "contenido": "string",
  "fecha_publicacion": "datetime",
  "likes": "integer",
  "comentarios": "integer", 
  "compartidos": "integer",
  "tipo_contenido": "string",
  "hashtags": "string",
  "menciones": "integer"
}
```

### 📈 **Estructura de Datos - Métricas**
```json
{
  "id_metrica": "integer",
  "id_usuario": "integer",
  "seguidores": "integer",
  "siguiendo": "integer", 
  "publicaciones_totales": "integer",
  "engagement_rate": "float",
  "alcance_promedio": "integer",
  "impresiones": "integer",
  "hora": "datetime"
}
```

### 👥 **Estructura de Datos - Usuarios**
```json
{
  "id_usuario": "integer",
  "cuenta": "string",
  "empresa_id": "integer",
  "fecha_creacion": "datetime",
  "activo": "boolean",
  "rol": "enum[admin,user,viewer]",
  "ultimo_acceso": "datetime"
}
```

---

## 🎯 Casos de Uso Reales

### 📊 **Para Analistas de Marketing Digital**

#### 🔮 **Predicciones de Crecimiento**
```bash
# Predecir seguidores para los próximos 30 días
GET /regression/predict/Interbank?dias=30

# Obtener métricas de precisión del modelo
GET /regression/metrics/Interbank
```

#### 📈 **Análisis de Tendencias**
```bash
# Agrupar publicaciones por patrones de engagement
POST /clustering/predict/BCPComunica
{
  "likes": 1500,
  "comentarios": 89,
  "compartidos": 234
}
```

### 🏢 **Para Gerentes de Social Media**

#### 📊 **Dashboard Empresarial**
```bash
# Ver todas las métricas de cuentas de la empresa
GET /crud/metricas/empresa_usuarios

# Comparar rendimiento entre cuentas
GET /regression/compare-models/CuentaA
```

#### 🎯 **Optimización de Contenido**
```bash
# Entrenar modelo con datos actualizados
GET /regression/train/MiCuentaEmpresa

# Identificar clusters de contenido exitoso
GET /clustering/clusters/MiCuentaEmpresa
```

### 🔍 **Para Administradores IT**

#### 👥 **Gestión de Usuarios**
```bash
# Listar usuarios de la empresa
GET /regression/users

# Monitorear estado de modelos
GET /regression/model-info/TodasLasCuentas
```

#### 📈 **Monitoreo y Auditoría**
```bash
# Historial de entrenamientos
GET /regression/history/CuentaEspecifica

# Estado de todos los modelos
GET /clustering/metrics/TodasLasCuentas
```

---

## 🏗️ Arquitectura

### **Flujo de Request Completo**
```
📱 Cliente (Browser/App)
    ↓ HTTP Request + JWT
🌐 FastAPI Application (main.py)
    ↓ Route Matching
🔗 Router Específico (/auth, /regression, /clustering, /crud)
    ↓ Middleware
🔐 JWT Verification (auth_required dependency)
    ↓ Authorization
🏢 Multi-tenant Check (empresa_id validation)
    ↓ Business Logic
🤖 ML Engine (scikit-learn models)
    ↓ Data Access
🗄️ DuckDB Analytics Database
    ↓ Response
📊 JSON Response + HTTP Status
    ↓
📱 Cliente recibe respuesta
```

### **Arquitectura de Componentes**
```
📁 app/
├── 🚀 main.py (FastAPI App)
├── 🔗 api/ (Routers)
│   ├── auth_routes.py
│   ├── regression.py
│   ├── routes_regression.py  
│   ├── clustering.py
│   ├── routes_cluster.py
│   └── routes_crud.py
├── 🔐 auth/ (JWT System)
│   ├── jwt_config.py
│   ├── auth_service.py
│   └── dependencies.py
└── 🗄️ database/ (DB Layer)
    └── connection.py

📁 models/ (ML Models)
├── user1_regression_model.pkl
├── user2_clustering_model.pkl
└── ...

📁 data/ (Database)
└── social_media.duckdb
```

---

## 🔗 Endpoints Principales

### 🔐 **Autenticación**
```
POST /auth/login
├── Body: {"username": "string", "password": "string"}
├── Response: {"access_token": "jwt_token", "token_type": "bearer"}
└── Status: 200 OK / 401 Unauthorized
```

### 📈 **Regresión (Machine Learning)**
```
GET /regression/predict/{username}
├── Headers: Authorization: Bearer {token}
├── Query: ?fecha=2025-07-15&dias=30
├── Response: {"prediction": 15420, "confidence": 0.85}
└── Status: 200 OK / 401 Unauthorized / 403 Forbidden

GET /regression/train/{username}  
├── Headers: Authorization: Bearer {token}
├── Response: {"model_id": "uuid", "r2_score": 0.92, "mae": 156.2}
└── Status: 200 OK / 401 Unauthorized / 403 Forbidden

GET /regression/metrics/{username}
├── Response: {"r2": 0.89, "mae": 234.1, "rmse": 345.6}
└── Status: 200 OK / 404 Not Found
```

### 🎯 **Clustering**
```
POST /clustering/predict/{username}
├── Headers: Authorization: Bearer {token}
├── Body: {"likes": 1200, "comentarios": 45, "compartidos": 78}
├── Response: {"cluster": 2, "cluster_name": "Alto Engagement"}
└── Status: 200 OK / 401 Unauthorized / 403 Forbidden

GET /clustering/clusters/{username}
├── Response: {"clusters": [{"id": 0, "name": "Bajo", "count": 234}]}
└── Status: 200 OK / 404 Not Found
```

### 📊 **CRUD de Datos**
```
GET /crud/publicaciones/{usuario}
├── Headers: Authorization: Bearer {token}
├── Response: [{"id": 1, "contenido": "...", "likes": 1234}]
└── Status: 200 OK / 401 Unauthorized / 403 Forbidden / 404 Not Found

GET /crud/metricas/{usuario}
├── Headers: Authorization: Bearer {token}  
├── Response: [{"seguidores": 15000, "engagement": 3.2}]
└── Status: 200 OK / 401 Unauthorized / 403 Forbidden / 404 Not Found
```

---

## 🔐 Autenticación

### **Sistema JWT Completo**

#### 🔑 **Proceso de Login**
```python
# 1. Cliente envía credenciales
POST /auth/login
{
  "username": "admin",
  "password": "password123"
}

# 2. Servidor valida y retorna JWT
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}

# 3. Cliente usa token en requests
GET /regression/predict/Interbank
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 🏢 **Control Multi-Empresa**
```python
# Usuarios por empresa
TechCorp: ["admin", "user"] → Acceso: ["BCPComunica", "bbva_peru", "Interbank"] 
DataInc: ["viewer"] → Acceso: ["BanBif", "ScotiabankPE"]
StartupXYZ: ["inactive"] → Acceso: ["BancodelaNacion", "BancoPichincha"]
```

#### 🛡️ **Niveles de Seguridad**
```
❌ Sin Token → 401 Unauthorized
❌ Token Inválido → 401 Unauthorized  
❌ Token Expirado → 401 Unauthorized
❌ Sin Acceso Empresa → 403 Forbidden
✅ Token Válido + Acceso → 200 OK
```

---

## 📈 Escalabilidad

### **Diseño Horizontal**
- **Por Empresa:** Cada empresa maneja sus propios modelos ML
- **Por Usuario:** Modelos individuales por cuenta social
- **Aislamiento:** Datos completamente separados entre empresas

### **Optimización de Performance**
- **DuckDB:** Base de datos columnar optimizada para analytics
- **Model Caching:** Modelos ML serializados en disco
- **Async FastAPI:** Operaciones no-bloqueantes
- **Connection Pooling:** Reutilización de conexiones DB

### **Monitoreo y Observabilidad**
- **Health Checks:** Endpoints de estado de la API
- **Model Metrics:** Métricas de rendimiento ML en tiempo real
- **Audit Logs:** Historial completo de operaciones
- **Error Tracking:** Manejo robusto de errores

---

## 🚀 Instalación y Uso

### **1. Instalación Local**
```bash
# Clonar repositorio
git clone <repository>
cd social-media-prediction-model

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### **2. Configuración Base de Datos**
```bash
# Ejecutar scripts de inicialización
python -c "
import duckdb
con = duckdb.connect('data/base_de_datos/social_media.duckdb')
con.execute(open('data/base_de_datos/scripts/createtable.sql').read())
con.execute(open('data/base_de_datos/scripts/insercioninsert.sql').read())
con.close()
"
```

### **3. Iniciar Servidor**
```bash
# Opción 1: Script personalizado
python start_server.py

# Opción 2: Uvicorn directo
uvicorn app.main:app --host localhost --port 8000 --reload

# Opción 3: Python module
python -m uvicorn app.main:app --reload
```

### **4. Verificar Instalación**
```bash
# Verificar endpoints protegidos
python check_crud_protection.py

# Prueba completa de autenticación
python test_crud_endpoints_jwt.py

# Documentación automática
# Abrir: http://localhost:8000/docs
```

### **5. Primer Uso**
```bash
# 1. Obtener token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'

# 2. Usar API protegida
curl -X GET "http://localhost:8000/regression/predict/Interbank" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 3. Explorar documentación
# http://localhost:8000/docs
```

---

## 🎯 Ventajas Competitivas

### ✅ **No-Code Machine Learning**
Los usuarios de negocio pueden entrenar y usar modelos ML sin programar

### ✅ **Enterprise Security**  
JWT + Multi-tenant + Role-based access control

### ✅ **Real-time Analytics**
Predicciones instantáneas optimizadas para performance

### ✅ **Industry Specific**
Diseñado específicamente para social media del sector financiero peruano

### ✅ **Auto-Documentation**
Swagger UI generado automáticamente con ejemplos interactivos

### ✅ **Audit Trail Completo**
Historial detallado de todos los modelos, predicciones y accesos

---

## 📞 Soporte y Documentación

### 📚 **Documentación Técnica**
- `DOCUMENTACION_JWT_COMPLETA.md` - Guía completa de autenticación
- `README_JWT.md` - Quick start guide
- `SOLUCION_CONTROL_ACCESO.md` - Configuración multi-empresa

### 🧪 **Scripts de Prueba**
- `test_crud_endpoints_jwt.py` - Pruebas completas de CRUD
- `demo_jwt_sistema.py` - Demo interactivo del sistema
- `check_crud_protection.py` - Verificación de seguridad

### 🔧 **Resolución de Problemas**
- `GUIA_SOLUCION_UVICORN.md` - Problemas comunes de servidor
- `diagnose_imports.py` - Debug de importaciones
- `minimal_app.py` - Versión mínima para testing

---

**Esta API representa una solución completa de Machine Learning empresarial para analytics de redes sociales, con seguridad, escalabilidad y facilidad de uso como pilares fundamentales.** 🚀
