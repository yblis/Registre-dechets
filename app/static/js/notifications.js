document.addEventListener('DOMContentLoaded', function() {
    // Initialiser tous les toasts
    const toastElList = document.querySelectorAll('.toast');
    const toastList = [...toastElList].map(toastEl => {
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000 // Disparaît après 5 secondes
        });
        
        // Montrer le toast automatiquement
        toast.show();
        
        return toast;
    });
    
    // Gérer la fermeture des toasts en cliquant sur le bouton de fermeture
    document.querySelectorAll('.toast .btn-close').forEach(function(closeButton) {
        closeButton.addEventListener('click', function() {
            const toast = bootstrap.Toast.getInstance(this.closest('.toast'));
            if (toast) {
                toast.hide();
            }
        });
    });
    
    // Animation d'entrée pour les toasts
    document.querySelectorAll('.toast').forEach(function(toast, index) {
        // Ajouter un délai entre l'apparition de chaque toast
        setTimeout(() => {
            toast.style.transition = 'transform 0.3s ease-in-out, opacity 0.3s ease-in-out';
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        }, index * 150);
    });
    
    // Nettoyer le container après que tous les toasts ont été fermés
    document.querySelectorAll('.toast').forEach(function(toast) {
        toast.addEventListener('hidden.bs.toast', function() {
            this.remove();
            
            // Si c'est le dernier toast, supprimer le conteneur
            const container = document.querySelector('.toast-container');
            if (container && container.querySelectorAll('.toast').length === 0) {
                container.remove();
            }
        });
    });
});