// Copyright (c) 2024, [Tu Nombre] and contributors
// For license information, please see license.txt

frappe.ui.form.on('Analisis Redes Sociales', {
    refresh: function(frm) {
        // Agregar botón para ejecutar análisis
        if (frm.doc.estado !== 'Completado') {
            frm.add_custom_button(__('Ejecutar Análisis'), function() {
                ejecutar_analisis(frm);
            }, __('Acciones'));
        }
        
        // Agregar botón para ver dashboard
        if (frm.doc.estado === 'Completado') {
            frm.add_custom_button(__('Ver Dashboard'), function() {
                window.open('/dashboard', '_blank');
            }, __('Ver Resultados'));
        }
        
        // Agregar botón para probar conexión API
        if (frm.doc.api_configuration) {
            frm.add_custom_button(__('Probar Conexión API'), function() {
                probar_conexion_api(frm);
            }, __('API'));
        }
        
        // Agregar botón de ejecución directa (para desarrollo)
        if (frm.doc.estado !== "Completado") {
            frm.add_custom_button(__('Ejecutar Directo (Dev)'), function() {
                frappe.show_alert({
                    message: 'Iniciando ejecución directa...',
                    indicator: 'blue'
                });
                
                frappe.call({
                    method: 'modulo_redes_sociales.modulo_redes_sociales.api.ejecutar_analisis_directo',
                    args: {
                        analisis_id: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            if (r.message.success) {
                                frappe.show_alert({
                                    message: `✅ ${r.message.message}`,
                                    indicator: 'green'
                                });
                                frm.reload_doc();
                            } else {
                                frappe.show_alert({
                                    message: `❌ Error: ${r.message.message}`,
                                    indicator: 'red'
                                });
                                frm.reload_doc();
                            }
                        }
                    },
                    error: function(xhr, status, error) {
                        frappe.show_alert({
                            message: `❌ Error de conexión: ${error}`,
                            indicator: 'red'
                        });
                    }
                });
            }, __('Acciones'));
        }
        
        // Actualizar visibilidad de campos
        actualizar_visibilidad_campos(frm);
    },
    
    tipo_analisis: function(frm) {
        // Actualizar visibilidad cuando cambia el tipo de análisis
        actualizar_visibilidad_campos(frm);
        
        // Limpiar campos que no aplican al nuevo tipo
        limpiar_campos_no_aplicables(frm);
    },
    
    api_configuration: function(frm) {
        // Cuando cambia la configuración de API, mostrar información
        if (frm.doc.api_configuration) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'API Configuration',
                    name: frm.doc.api_configuration
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.show_alert({
                            message: __('API configurada: ') + r.message.api_name + ' (' + r.message.base_url + ')',
                            indicator: 'blue'
                        });
                    }
                }
            });
        }
    }
});

function actualizar_visibilidad_campos(frm) {
    const tipo = frm.doc.tipo_analisis;
    
    // Campo específico para Predicción de Seguidores (en parámetros)
    if (frm.fields_dict['fecha_analisis']) {
        frm.toggle_display('fecha_analisis', tipo === 'Predicción de Seguidores');
    }
    
    // Campos específicos de Clustering
    const campos_clustering = [
        'clustering_section', 'likes', 'comentarios', 'compartidos',
        'cluster_resultado', 'cluster_asignado', 'cluster_nombre'
    ];
    
    // Mostrar/ocultar campos de clustering
    campos_clustering.forEach(campo => {
        if (frm.fields_dict[campo]) {
            frm.toggle_display(campo, tipo === 'Clustering');
        }
    });
    
    // Campo de métricas para entrenamiento y métricas de modelo
    if (frm.fields_dict['metricas_modelo']) {
        frm.toggle_display('metricas_modelo', 
            tipo === 'Entrenamiento de Modelo' || tipo === 'Métricas de Modelo');
    }
    
    // Campo de predicción de seguidores en resultados
    if (frm.fields_dict['prediccion_seguidores']) {
        frm.toggle_display('prediccion_seguidores', tipo === 'Predicción de Seguidores');
    }
}

function limpiar_campos_no_aplicables(frm) {
    const tipo = frm.doc.tipo_analisis;
    
    if (tipo !== 'Predicción de Seguidores') {
        frm.set_value('fecha_analisis', '');
    }
    
    if (tipo !== 'Clustering') {
        frm.set_value('likes', '');
        frm.set_value('comentarios', '');
        frm.set_value('compartidos', '');
    }
    
    if (tipo !== 'Entrenamiento de Modelo' && tipo !== 'Métricas de Modelo') {
        frm.set_value('metricas_modelo', '');
    }
}

function ejecutar_analisis(frm) {
    if (!frm.doc.titulo || !frm.doc.tipo_analisis || !frm.doc.usuario_red_social || !frm.doc.api_configuration) {
        frappe.msgprint(__('Por favor complete todos los campos requeridos (incluida la Configuración de API).'));
        return;
    }
    
    frappe.confirm(
        __('¿Está seguro de que desea ejecutar este análisis?'),
        function() {
            frm.set_value('estado', 'Ejecutando');
            frm.save().then(() => {
                frappe.call({
                    method: 'modulo_redes_sociales.modulo_redes_sociales.api.ejecutar_analisis',
                    args: {
                        analisis_id: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message && r.message.success) {
                            frappe.show_alert({
                                message: __('Análisis iniciado correctamente'),
                                indicator: 'green'
                            });
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Error al iniciar el análisis: ') + (r.message ? r.message.error : 'Error desconocido'));
                            frm.set_value('estado', 'Error');
                            frm.save();
                        }
                    },
                    error: function() {
                        frappe.msgprint(__('Error de conexión al ejecutar el análisis'));
                        frm.set_value('estado', 'Error');
                        frm.save();
                    }
                });
            });
        }
    );
}

function probar_conexion_api(frm) {
    if (!frm.doc.api_configuration) {
        frappe.msgprint(__('Por favor seleccione una Configuración de API primero.'));
        return;
    }
    
    frappe.call({
        method: 'modulo_redes_sociales.modulo_redes_sociales.doctype.api_configuration.api_configuration.test_connection',
        args: {
            api_config_name: frm.doc.api_configuration
        },
        callback: function(r) {
            if (r.message && r.message.success) {
                frappe.show_alert({
                    message: __('Conexión exitosa con la API'),
                    indicator: 'green'
                });
            } else {
                frappe.msgprint({
                    title: __('Error de Conexión'),
                    message: __('No se pudo conectar con la API: ') + (r.message ? r.message.error : 'Error desconocido'),
                    indicator: 'red'
                });
            }
        },
        error: function() {
            frappe.msgprint({
                title: __('Error de Conexión'),
                message: __('Error al intentar conectar con la API'),
                indicator: 'red'
            });
        }
    });
}
