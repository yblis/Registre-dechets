document.addEventListener('DOMContentLoaded', function() {
    // Récupérer le token CSRF depuis la méta balise
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Configuration par défaut pour fetch avec le token CSRF
    function fetchWithCSRF(url, options = {}) {
        const defaultOptions = {
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        };
        return fetch(url, { ...defaultOptions, ...options });
    }

    // Gestionnaires pour les formulaires de référence
    function handleReferenceForm(formId, modalId, selectId) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            fetchWithCSRF(this.action, {
                method: 'POST',
                body: new FormData(this)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Ajouter la nouvelle option au select
                    const select = document.getElementById(selectId);
                    const option = new Option(data.label, data.id, true, true);
                    select.add(option);

                    // Fermer la modal et réinitialiser le formulaire
                    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
                    modal.hide();
                    form.reset();
                } else {
                    alert(data.error || 'Une erreur est survenue');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Une erreur est survenue lors de la communication avec le serveur');
            });
        });
    }

    // Formatage automatique des champs SIRET
    function setupSiretFormatting() {
        document.querySelectorAll('input[name="siret"]').forEach(function(input) {
            input.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 14) value = value.slice(0, 14);
                e.target.value = value;
            });
        });
    }

    // Initialisation des gestionnaires de formulaire
    handleReferenceForm('newProducerForm', 'addProducerModal', 'producer_id');
    handleReferenceForm('newTransporterForm', 'addTransporterModal', 'transporter_id');
    
    // Initialisation du formatage des champs
    setupSiretFormatting();

    // Gérer l'affichage des erreurs de validation
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});
