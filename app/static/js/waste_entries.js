function addWasteEntry() {
    const container = document.getElementById('waste-entries-container');
    const entryCount = container.getElementsByClassName('waste-entry').length;
    const template = document.createElement('div');
    template.className = 'waste-entry row g-3 mb-4 p-3 border rounded bg-light position-relative';
    template.setAttribute('data-entry-index', entryCount);
    
    // Create the header template with the correct entry number
    const headerHTML = `
        <div class="waste-entry-header mb-2 pb-2 border-bottom w-100">
            <h5 class="fw-bold text-primary mb-0">
                Type de déchet #<span class="waste-entry-number">${entryCount + 1}</span>
            </h5>
        </div>
    `;
    
    // Clone the first entry's HTML but update the indices
    const firstEntry = container.querySelector('.waste-entry');
    if (firstEntry) {
        // Get the content of the first entry except the header
        let contentHTML = firstEntry.innerHTML;
        // Remove the header part if it exists
        const headerEndIndex = contentHTML.indexOf('</div>') + 6; // Length of "</div>"
        if (headerEndIndex > 5) {
            contentHTML = contentHTML.substring(headerEndIndex).trim();
        }
        
        // Replace the indices in the form fields
        let newHTML = contentHTML.replace(/waste_entries-0/g, `waste_entries-${entryCount}`);
        
        // Set the full HTML with the new header and content
        template.innerHTML = headerHTML + newHTML;
        
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
        
        // Animate the new entry to draw attention to it
        template.style.transition = 'background-color 0.5s ease';
        template.style.backgroundColor = '#e8f4ff';
        setTimeout(() => {
            template.style.backgroundColor = '';
        }, 1000);
    }
}

function removeWasteEntry(button) {
    const container = document.getElementById('waste-entries-container');
    const entries = container.getElementsByClassName('waste-entry');
    
    // Don't remove if it's the last entry
    if (entries.length > 1) {
        const entry = button.closest('.waste-entry');
        entry.remove();
        
        // Update numbering of remaining entries
        Array.from(entries).forEach((entry, index) => {
            // Update data-entry-index attribute
            entry.setAttribute('data-entry-index', index);
            
            // Update entry number in the header
            const numberSpan = entry.querySelector('.waste-entry-number');
            if (numberSpan) {
                numberSpan.textContent = index + 1;
            }
            
            // Update form field indices
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
