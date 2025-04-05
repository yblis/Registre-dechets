function addWasteEntry() {
    const container = document.getElementById('waste-entries-container');
    const entryCount = container.getElementsByClassName('waste-entry').length;
    const template = document.createElement('div');
    template.className = 'waste-entry row g-3 mb-3 pb-3 border-bottom';
    
    // Clone the first entry's HTML but update the indices
    const firstEntry = container.querySelector('.waste-entry');
    if (firstEntry) {
        const html = firstEntry.innerHTML.replace(/waste_entries-0/g, `waste_entries-${entryCount}`);
        template.innerHTML = html;
        
        // Clear any values in the cloned form except treatment and elimination operation selects
        template.querySelectorAll('input, select').forEach(input => {
            const isOperationSelect = input.name && (
                input.name.includes('treatment_operation_id') || 
                input.name.includes('elimination_operation_id')
            );
            if (input.type === 'number' || !isOperationSelect) {
                input.value = '';
            }
        });
        
        container.appendChild(template);
    }
}

function removeWasteEntry(button) {
    const container = document.getElementById('waste-entries-container');
    const entries = container.getElementsByClassName('waste-entry');
    
    // Don't remove if it's the last entry
    if (entries.length > 1) {
        const entry = button.closest('.waste-entry');
        entry.remove();
        
        // Reindex remaining entries
        Array.from(entries).forEach((entry, index) => {
            entry.innerHTML = entry.innerHTML.replace(/waste_entries-\d+/g, `waste_entries-${index}`);
        });
    } else {
        // If it's the last entry, just clear the values
        const entry = entries[0];
        entry.querySelectorAll('input, select').forEach(input => {
            const isOperationSelect = input.name && (
                input.name.includes('treatment_operation_id') || 
                input.name.includes('elimination_operation_id')
            );
            if (input.type === 'number' || !isOperationSelect) {
                input.value = '';
            } else if (input.tagName === 'SELECT' && !isOperationSelect) {
                input.selectedIndex = 0;
            }
        });
    }
}
