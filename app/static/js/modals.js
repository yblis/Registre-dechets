document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Configurer les modales pour qu'elles s'affichent correctement
    document.querySelectorAll('.modal').forEach(function(modal) {
        // Ajouter la classe modal-static pour éviter le scintillement
        modal.classList.add('modal-static');
        
        // Empêcher la propagation des événements
        modal.addEventListener('show.bs.modal', function(event) {
            event.stopPropagation();
        });
        
        // S'assurer que la modale est au-dessus de tout
        modal.style.zIndex = '1060';
        
        // Configurer les options de la modale
        var modalOptions = {
            backdrop: true,
            keyboard: true,
            focus: true
        };
        
        // Initialiser la modale avec les options
        var modalInstance = new bootstrap.Modal(modal, modalOptions);
    });
    
    // Ajouter un style pour s'assurer que les modales sont toujours visibles
    var style = document.createElement('style');
    style.innerHTML = `
        .modal-backdrop {
            z-index: 1050 !important;
        }
        .modal {
            z-index: 1055 !important;
        }
        .modal-dialog {
            z-index: 1056 !important;
        }
    `;
    document.head.appendChild(style);
});
