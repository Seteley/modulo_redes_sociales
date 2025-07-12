frappe.ui.form.on('API Configuration', {
    refresh: function(frm) {
        // Agregar botón personalizado para probar conexión
        if (!frm.doc.__islocal) {  // Solo si el documento ya está guardado
            frm.add_custom_button(__('Probar Conexión'), function() {
                test_api_connection(frm);
            }, __('Acciones'));
        }
    },
    
    // Validar URL cuando cambie
    api_url: function(frm) {
        if (frm.doc.api_url && !frm.doc.api_url.startsWith('http')) {
            frappe.msgprint('La URL debe comenzar con http:// o https://');
        }
    }
});

function test_api_connection(frm) {
    // Verificar que los campos requeridos estén llenos
    if (!frm.doc.api_url || !frm.doc.username || !frm.doc.password) {
        frappe.msgprint({
            title: 'Campos Requeridos',
            message: 'Por favor llena URL de la API, Usuario y Contraseña antes de probar la conexión.',
            indicator: 'orange'
        });
        return;
    }
    
    // Mostrar indicador de carga
    frappe.show_alert({
        message: 'Probando conexión con la API...',
        indicator: 'blue'
    });
    
    // Llamar al método del servidor
    frappe.call({
        method: 'test_connection_btn',
        doc: frm.doc,
        callback: function(r) {
            if (r.message) {
                frappe.show_alert({
                    message: '✅ Conexión exitosa con la API',
                    indicator: 'green'
                });
                
                frappe.msgprint({
                    title: '🎉 Prueba de Conexión',
                    message: '<div style="color: green; font-size: 14px;"><strong>¡Conexión exitosa!</strong><br><br>' +
                            'La configuración es correcta y ERPNext puede comunicarse con la API.<br><br>' +
                            '📋 <strong>Próximos pasos:</strong><br>' +
                            '• Crear un análisis en "Analisis Redes Sociales"<br>' +
                            '• Ver resultados en el Dashboard</div>',
                    indicator: 'green'
                });
                
                // Refrescar el formulario para ver campos actualizados
                frm.reload_doc();
            }
        },
        error: function(r) {
            let error_message = 'Error desconocido';
            if (r.exc) {
                // Extraer mensaje de error más limpio
                let exc_lines = r.exc.split('\n');
                for (let line of exc_lines) {
                    if (line.includes('frappe.exceptions.ValidationError:')) {
                        error_message = line.split('frappe.exceptions.ValidationError:')[1].trim();
                        break;
                    }
                }
            }
            
            frappe.show_alert({
                message: 'Error en la conexión',
                indicator: 'red'
            });
            
            frappe.msgprint({
                title: 'Error de Conexión',
                message: `No se pudo conectar con la API:<br><br><strong>${error_message}</strong><br><br>
                         Verifica que:<br>
                         • La URL sea correcta (http://172.25.128.1:8000)<br>
                         • El usuario y contraseña sean válidos<br>
                         • La API esté ejecutándose con --host 0.0.0.0`,
                indicator: 'red'
            });
        }
    });
}
