// Social Media Analytics Dashboard JavaScript

// Funciones principales del dashboard
window.SocialMediaAnalytics = {
    
    // Inicializar dashboard
    init: function() {
        this.setupEventListeners();
        this.loadDashboardData();
        this.startAutoRefresh();
    },
    
    // Configurar event listeners
    setupEventListeners: function() {
        // Event listener para botones de análisis rápido
        document.addEventListener('click', function(e) {
            if (e.target.matches('.quick-analysis-btn')) {
                const type = e.target.dataset.analysisType;
                SocialMediaAnalytics.showQuickAnalysisModal(type);
            }
        });
    },
    
    // Cargar datos del dashboard
    loadDashboardData: function() {
        frappe.call({
            method: 'modulo_redes_sociales.modulo_redes_sociales.api.get_dashboard_stats',
            callback: function(r) {
                if (r.message) {
                    SocialMediaAnalytics.updateDashboardStats(r.message);
                }
            }
        });
    },
    
    // Actualizar estadísticas del dashboard
    updateDashboardStats: function(stats) {
        // Actualizar números principales
        const elements = {
            'total-analisis': stats.total_analisis,
            'analisis-completados': stats.analisis_completados,
            'analisis-error': stats.analisis_error,
            'analisis-pendientes': stats.analisis_pendientes
        };
        
        Object.keys(elements).forEach(function(id) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = elements[id];
            }
        });
        
        // Actualizar gráfico por tipos si existe
        if (stats.por_tipo && typeof Chart !== 'undefined') {
            this.updateTypeChart(stats.por_tipo);
        }
    },
    
    // Mostrar modal de análisis rápido
    showQuickAnalysisModal: function(type) {
        const modal = document.getElementById('modalAnalisisRapido');
        if (!modal) return;
        
        // Configurar título y tipo
        document.getElementById('tipoAnalisis').value = type;
        document.getElementById('usuarioRedSocial').value = '';
        
        // Limpiar formulario anterior
        const parametrosDiv = document.getElementById('parametrosEspecificos');
        parametrosDiv.innerHTML = '';
        
        // Agregar campos específicos
        this.addSpecificFields(type, parametrosDiv);
        
        // Mostrar modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },
    
    // Agregar campos específicos según tipo de análisis
    addSpecificFields: function(type, container) {
        let html = '';
        
        switch(type) {
            case 'Predicción de Seguidores':
                html = `
                    <div class="mb-3">
                        <label class="form-label">Días para Predicción</label>
                        <input type="number" class="form-control" id="diasPrediccion" value="30" min="1" max="365">
                        <div class="form-text">Número de días en el futuro para hacer la predicción</div>
                    </div>
                `;
                break;
                
            case 'Clustering':
                html = `
                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Likes</label>
                            <input type="number" class="form-control" id="likes" required min="0">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Comentarios</label>
                            <input type="number" class="form-control" id="comentarios" required min="0">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Compartidos</label>
                            <input type="number" class="form-control" id="compartidos" required min="0">
                        </div>
                    </div>
                    <div class="alert alert-info">
                        <small>Ingrese las métricas de una publicación para determinar a qué cluster pertenece</small>
                    </div>
                `;
                break;
                
            case 'Entrenamiento de Modelo':
                html = `
                    <div class="alert alert-warning">
                        <strong>Atención:</strong> El entrenamiento del modelo puede tomar varios minutos.
                        Se procesará en segundo plano.
                    </div>
                `;
                break;
                
            case 'Métricas de Modelo':
                html = `
                    <div class="alert alert-info">
                        <strong>Información:</strong> Se obtendrán las métricas de rendimiento del modelo actual
                        (R², MAE, RMSE).
                    </div>
                `;
                break;
        }
        
        container.innerHTML = html;
    },
    
    // Ejecutar análisis rápido
    executeQuickAnalysis: function() {
        const type = document.getElementById('tipoAnalisis').value;
        const usuario = document.getElementById('usuarioRedSocial').value;
        
        if (!usuario) {
            this.showAlert('Por favor ingrese el usuario de red social', 'warning');
            return;
        }
        
        // Recopilar parámetros
        const params = {
            tipo_analisis: type,
            usuario_red_social: usuario
        };
        
        // Agregar parámetros específicos
        this.collectSpecificParams(type, params);
        
        // Mostrar loading
        const executeBtn = document.querySelector('#modalAnalisisRapido .btn-primary');
        const originalText = executeBtn.textContent;
        executeBtn.innerHTML = '<span class="loading-spinner"></span> Creando...';
        executeBtn.disabled = true;
        
        // Hacer llamada a la API
        frappe.call({
            method: 'modulo_redes_sociales.modulo_redes_sociales.api.create_quick_analysis',
            args: params,
            callback: function(r) {
                executeBtn.textContent = originalText;
                executeBtn.disabled = false;
                
                if (r.message && r.message.success) {
                    // Cerrar modal
                    bootstrap.Modal.getInstance(document.getElementById('modalAnalisisRapido')).hide();
                    
                    // Mostrar mensaje de éxito
                    SocialMediaAnalytics.showAlert('Análisis creado y en ejecución', 'success');
                    
                    // Recargar datos
                    setTimeout(() => {
                        SocialMediaAnalytics.loadDashboardData();
                        SocialMediaAnalytics.loadRecentAnalysis();
                    }, 1000);
                } else {
                    SocialMediaAnalytics.showAlert('Error al crear análisis: ' + (r.message?.message || 'Error desconocido'), 'error');
                }
            },
            error: function(r) {
                executeBtn.textContent = originalText;
                executeBtn.disabled = false;
                SocialMediaAnalytics.showAlert('Error de conexión: ' + r.message, 'error');
            }
        });
    },
    
    // Recopilar parámetros específicos del formulario
    collectSpecificParams: function(type, params) {
        switch(type) {
            case 'Predicción de Seguidores':
                const dias = document.getElementById('diasPrediccion')?.value;
                if (dias) params.dias_prediccion = parseInt(dias);
                break;
                
            case 'Clustering':
                const likes = document.getElementById('likes')?.value;
                const comentarios = document.getElementById('comentarios')?.value;
                const compartidos = document.getElementById('compartidos')?.value;
                
                if (likes) params.likes = parseInt(likes);
                if (comentarios) params.comentarios = parseInt(comentarios);
                if (compartidos) params.compartidos = parseInt(compartidos);
                break;
        }
    },
    
    // Cargar análisis recientes
    loadRecentAnalysis: function() {
        frappe.call({
            method: 'modulo_redes_sociales.modulo_redes_sociales.api.get_recent_analysis',
            args: { limit: 10 },
            callback: function(r) {
                if (r.message) {
                    SocialMediaAnalytics.updateRecentAnalysisTable(r.message);
                }
            }
        });
    },
    
    // Actualizar tabla de análisis recientes
    updateRecentAnalysisTable: function(analysis) {
        const tbody = document.querySelector('#recent-analysis-table tbody');
        if (!tbody) return;
        
        if (analysis.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay análisis registrados</td></tr>';
            return;
        }
        
        tbody.innerHTML = analysis.map(item => `
            <tr>
                <td>${item.titulo}</td>
                <td><span class="badge badge-outline-secondary">${item.tipo_analisis}</span></td>
                <td>${item.usuario_red_social}</td>
                <td><span class="status-badge ${this.getStatusClass(item.estado)}">${item.estado}</span></td>
                <td>${this.formatDateTime(item.fecha_creacion)}</td>
                <td>
                    <a href="/app/analisis-redes-sociales/${item.name}" class="btn btn-sm btn-outline-primary">Ver</a>
                </td>
            </tr>
        `).join('');
    },
    
    // Obtener clase CSS para estado
    getStatusClass: function(status) {
        const classes = {
            'Completado': 'success',
            'Error': 'error',
            'Pendiente': 'warning',
            'Ejecutando': 'info'
        };
        return classes[status] || 'info';
    },
    
    // Formatear fecha y hora
    formatDateTime: function(datetime) {
        if (!datetime) return '';
        const date = new Date(datetime);
        return date.toLocaleString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Mostrar alertas
    showAlert: function(message, type) {
        if (typeof frappe !== 'undefined' && frappe.show_alert) {
            frappe.show_alert({
                message: message,
                indicator: type === 'success' ? 'green' : type === 'error' ? 'red' : 'orange'
            });
        } else {
            alert(message);
        }
    },
    
    // Probar conexión con API
    testApiConnection: function() {
        const btn = document.getElementById('test-connection-btn');
        if (btn) {
            btn.innerHTML = '<span class="loading-spinner"></span> Probando...';
            btn.disabled = true;
        }
        
        frappe.call({
            method: 'modulo_redes_sociales.modulo_redes_sociales.api.test_api_connection',
            callback: function(r) {
                if (btn) {
                    btn.textContent = 'Probar Conexión';
                    btn.disabled = false;
                }
                
                if (r.message) {
                    const type = r.message.success ? 'success' : 'error';
                    SocialMediaAnalytics.showAlert(r.message.message, type);
                    
                    if (r.message.success) {
                        // Actualizar estado de la API en la UI
                        const statusElement = document.getElementById('api-status');
                        if (statusElement) {
                            statusElement.className = 'status-badge success';
                            statusElement.textContent = 'Exitoso';
                        }
                    }
                }
            }
        });
    },
    
    // Auto-refresh del dashboard
    startAutoRefresh: function() {
        setInterval(() => {
            this.loadDashboardData();
            this.loadRecentAnalysis();
        }, 30000); // Cada 30 segundos
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('/dashboard')) {
        SocialMediaAnalytics.init();
    }
});

// Funciones globales para el HTML
window.crearAnalisisRapido = function(tipo) {
    SocialMediaAnalytics.showQuickAnalysisModal(tipo);
};

window.ejecutarAnalisisRapido = function() {
    SocialMediaAnalytics.executeQuickAnalysis();
};

window.probarConexionAPI = function() {
    SocialMediaAnalytics.testApiConnection();
};
