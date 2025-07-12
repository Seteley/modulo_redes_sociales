// Navegación intuitiva para Social Media Analytics
$(document).ready(function() {
    // Agregar navegación rápida al header de ERPNext
    addQuickNavigation();
    
    // Atajos de teclado
    setupKeyboardShortcuts();
    
    // Menú contextual
    setupContextMenu();
});

function addQuickNavigation() {
    // Agregar menú dropdown en la barra superior
    const navHtml = `
        <li class="dropdown" id="social-media-nav">
            <a class="dropdown-toggle" data-toggle="dropdown" href="#" style="color: #2ecc71;">
                <i class="fa fa-share-alt-square"></i> Social Media
            </a>
            <ul class="dropdown-menu">
                <li><a href="/app/api-configuration"><i class="fa fa-cog"></i> Configurar API</a></li>
                <li><a href="/app/analisis-redes-sociales"><i class="fa fa-list"></i> Ver Análisis</a></li>
                <li><a href="/app/analisis-redes-sociales/new"><i class="fa fa-plus"></i> Nuevo Análisis</a></li>
                <li class="divider"></li>
                <li><a href="/dashboard"><i class="fa fa-dashboard"></i> Dashboard</a></li>
                <li><a href="http://172.25.128.1:8000/docs" target="_blank"><i class="fa fa-book"></i> API Docs</a></li>
            </ul>
        </li>
    `;
    
    // Insertar en la barra de navegación
    setTimeout(function() {
        if ($('.navbar-nav').length && !$('#social-media-nav').length) {
            $('.navbar-nav').append(navHtml);
        }
    }, 1000);
}

function setupKeyboardShortcuts() {
    $(document).on('keydown', function(e) {
        // Alt + S: Menú Social Media
        if (e.altKey && e.which === 83) {
            e.preventDefault();
            $('#social-media-nav .dropdown-toggle').dropdown('toggle');
        }
        // Alt + 1: API Config
        else if (e.altKey && e.which === 49) {
            e.preventDefault();
            window.location.href = '/app/api-configuration';
        }
        // Alt + 2: Nuevo Análisis
        else if (e.altKey && e.which === 50) {
            e.preventDefault();
            window.location.href = '/app/analisis-redes-sociales/new';
        }
        // Alt + 3: Lista Análisis
        else if (e.altKey && e.which === 51) {
            e.preventDefault();
            window.location.href = '/app/analisis-redes-sociales';
        }
        // Alt + D: Dashboard
        else if (e.altKey && e.which === 68) {
            e.preventDefault();
            window.location.href = '/dashboard';
        }
    });
}

function setupContextMenu() {
    // Agregar botón flotante
    const floatingButton = `
        <div id="social-media-floating" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            background: #3498db;
            border-radius: 50px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            color: white;
            font-size: 20px;
        " title="Social Media Analytics (Alt+S)">
            <i class="fa fa-share-alt-square"></i>
        </div>
        
        <div id="floating-menu" style="
            position: fixed;
            bottom: 80px;
            right: 20px;
            z-index: 9998;
            background: white;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: none;
            min-width: 200px;
        ">
            <div style="padding: 5px 0;">
                <a href="/app/api-configuration" style="display: block; padding: 8px; text-decoration: none; color: #333; border-radius: 5px;" 
                   onmouseover="this.style.backgroundColor='#f8f9fa'" onmouseout="this.style.backgroundColor='transparent'">
                    🔧 Configurar API
                </a>
                <a href="/app/analisis-redes-sociales/new" style="display: block; padding: 8px; text-decoration: none; color: #333; border-radius: 5px;"
                   onmouseover="this.style.backgroundColor='#f8f9fa'" onmouseout="this.style.backgroundColor='transparent'">
                    ➕ Nuevo Análisis
                </a>
                <a href="/app/analisis-redes-sociales" style="display: block; padding: 8px; text-decoration: none; color: #333; border-radius: 5px;"
                   onmouseover="this.style.backgroundColor='#f8f9fa'" onmouseout="this.style.backgroundColor='transparent'">
                    📊 Ver Análisis
                </a>
                <hr style="margin: 5px 0;">
                <a href="/dashboard" style="display: block; padding: 8px; text-decoration: none; color: #333; border-radius: 5px;"
                   onmouseover="this.style.backgroundColor='#f8f9fa'" onmouseout="this.style.backgroundColor='transparent'">
                    📈 Dashboard
                </a>
            </div>
        </div>
    `;
    
    // Agregar botón flotante después de cargar la página
    setTimeout(function() {
        if (!$('#social-media-floating').length) {
            $('body').append(floatingButton);
            
            // Toggle del menú flotante
            $('#social-media-floating').on('click', function() {
                $('#floating-menu').toggle();
            });
            
            // Cerrar menú al hacer clic fuera
            $(document).on('click', function(e) {
                if (!$(e.target).closest('#social-media-floating, #floating-menu').length) {
                    $('#floating-menu').hide();
                }
            });
        }
    }, 2000);
}

// Funciones globales para uso desde cualquier parte
window.goToSocialMediaConfig = function() {
    window.location.href = '/app/api-configuration';
};

window.createSocialMediaAnalysis = function() {
    window.location.href = '/app/analisis-redes-sociales/new';
};

window.viewSocialMediaAnalysis = function() {
    window.location.href = '/app/analisis-redes-sociales';
};

window.goToSocialMediaDashboard = function() {
    window.location.href = '/dashboard';
};
