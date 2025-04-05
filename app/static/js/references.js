document.addEventListener('DOMContentLoaded', function() {
    // Gestion des modales de modification
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(function(element) {
        element.addEventListener('click', function() {
            const modal = document.querySelector(this.dataset.bsTarget);
            if (modal && this.dataset.values) {
                const values = JSON.parse(this.dataset.values);
                modal.querySelectorAll('input, textarea, select').forEach(function(input) {
                    if (values[input.name]) {
                        if (input.type === 'checkbox') {
                            input.checked = values[input.name];
                        } else {
                            input.value = values[input.name];
                        }
                    }
                });
            }
        });
    });

    // Validation des formulaires
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Gestion des tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Formatage des champs SIRET
    document.querySelectorAll('input[name="siret"]').forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 14) value = value.slice(0, 14);
            e.target.value = value;
        });
    });

    // Mise en majuscules automatique pour les codes
    document.querySelectorAll('input[name="code"]').forEach(function(input) {
        input.addEventListener('input', function(e) {
            e.target.value = e.target.value.toUpperCase();
        });
    });

    // Confirmation de suppression
    document.querySelectorAll('form[data-confirm]').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Affichage du nombre d'enregistrements sélectionnés
    document.querySelectorAll('.table').forEach(function(table) {
        const checkboxes = table.querySelectorAll('input[type="checkbox"]');
        const counter = table.querySelector('.selected-counter');
        
        if (counter) {
            checkboxes.forEach(function(checkbox) {
                checkbox.addEventListener('change', function() {
                    const selected = table.querySelectorAll('input[type="checkbox"]:checked').length;
                    counter.textContent = selected + ' élément(s) sélectionné(s)';
                    counter.style.display = selected > 0 ? 'block' : 'none';
                });
            });
        }
    });

    // Gestion du tri des tableaux
    document.querySelectorAll('.sortable').forEach(function(th) {
        th.addEventListener('click', function() {
            const table = th.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const index = Array.from(th.parentNode.children).indexOf(th);
            const direction = th.classList.contains('asc') ? -1 : 1;

            // Mettre à jour les classes de tri
            th.closest('tr').querySelectorAll('th').forEach(header => header.classList.remove('asc', 'desc'));
            th.classList.toggle('asc', direction === 1);
            th.classList.toggle('desc', direction === -1);

            // Trier les lignes
            rows.sort((a, b) => {
                const aValue = a.children[index].textContent.trim();
                const bValue = b.children[index].textContent.trim();
                return aValue.localeCompare(bValue, undefined, {numeric: true}) * direction;
            });

            // Réorganiser le tableau
            tbody.append(...rows);
        });
    });
});
