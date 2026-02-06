
document.addEventListener('DOMContentLoaded', () => {
    const wardId = "{{ ward-id }}";
    const storageKey = `vote_demo_worksheet_notes_${wardId}`;

    // Load notes
    let notes = {};
    try {
        const saved = localStorage.getItem(storageKey);
        if (saved) notes = JSON.parse(saved);
    } catch (e) { console.error("Could not load notes", e); }

    const textareas = document.querySelectorAll('.worksheet-note-area');
    const emojiSelectors = document.querySelectorAll('.emoji-selector-button');

    // Apply initial notes
    textareas.forEach(ta => {
        const id = ta.getAttribute('data-nominee-id');
        if (notes[id]) ta.value = notes[id];
        
        let debounceTimer;
        ta.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            console.log("Saving notes for " + id);
            notes[id] = e.target.value;
            localStorage.setItem(storageKey, JSON.stringify(notes));
        }, 500);
        });
    });

    emojiSelectors.forEach(selector => {
        const parent = selector.parentNode;
        const id = parent.getAttribute('nominee-id');
        // Initial state
        if (notes[id] == selector.innerText) {
        selector.classList.add("emoji-selector-button-selected");
        document.querySelector(`span[nominee-id="${id}"]`).innerText = selector.innerText;
        } else {
        selector.classList.remove("emoji-selector-button-selected");
        }

        selector.addEventListener('click', (e) => {
        const id = parent.getAttribute('nominee-id');
        
        // Remove from siblings
        Array.from(parent.children).forEach(child => {
            child.classList.remove("emoji-selector-button-selected");
        });

        // Add to clicked
        selector.classList.add("emoji-selector-button-selected");
        document.querySelector(`span[nominee-id="${id}"]`).innerText = selector.innerText;
        
        notes[id] = e.target.innerText;
        localStorage.setItem(storageKey, JSON.stringify(notes));
        });
    });

    // Handle Export
    document.getElementById('export-btn').addEventListener('click', () => {
        if (Object.keys(notes).length === 0) {
        alert("No notes to export!");
        return;
        }

        let csvContent = "NomineeID,Name,Note\n";
        textareas.forEach(ta => {
        const id = ta.getAttribute('data-nominee-id');
        const name = ta.getAttribute('data-nominee-name');
        if (notes[id]) {
            const safeNote = `"${notes[id].replace(/"/g, '""')}"`;
            csvContent += `${id},"${name}",${safeNote}\n`;
        }
        });

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", `worksheet_notes_${wardId}.csv`);
        link.click();
    });

    // Handle Import
    const importFile = document.getElementById('import-file');
    document.getElementById('import-btn').addEventListener('click', () => importFile.click());

    importFile.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (evt) => {
        const lines = evt.target.result.split('\n');
        let importedCount = 0;
        lines.forEach((line, idx) => {
            if (idx === 0 || !line.trim()) return;
            const parts = line.split(',');
            if (parts.length >= 3) {
            const id = parts[0];
            let note = parts.slice(2).join(',');
            if (note.startsWith('"') && note.endsWith('"')) {
                note = note.substring(1, note.length - 1).replace(/""/g, '"');
            }
            notes[id] = note;
            
            const ta = document.querySelector(`.worksheet-note-area[data-nominee-id="${id}"]`);
            if (ta) ta.value = note;
            importedCount++;
            }
        });
        localStorage.setItem(storageKey, JSON.stringify(notes));
        alert(`Successfully imported ${importedCount} notes.`);
        };
        reader.readAsText(file);
    });
});