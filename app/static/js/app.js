// app/static/js/app.js
document.addEventListener('DOMContentLoaded', function () {
    console.log('MusicApp Edu cargado');

    // Animación suave para botones
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.opacity = '0.9';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.opacity = '1';
        });
    });

    // Confirmación antes de borrar
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (!confirm('¿Seguro que quieres eliminar esto?')) {
                e.preventDefault();
            }
        });
    });

    // Cerrar alertas
    const alerts = document.querySelectorAll('.alert');
    setTimeout(() => {
        alerts.forEach(alert => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});