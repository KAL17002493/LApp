let wordBatchToDelete = JSON.parse(sessionStorage.getItem('wordBatchToDelete')) || []; // Load batch from sessionStorage or initialize an empty array
let wordCount = parseInt(document.getElementById('wordCount').innerText);

function addToDeleteBatch(itemId) {
    wordBatchToDelete.push(itemId);
    sessionStorage.setItem('wordBatchToDelete', JSON.stringify(wordBatchToDelete));
}

function handleDelete(itemId) {
    addToDeleteBatch(itemId);
    document.getElementById(`item-${itemId}`).style.display = 'none'; // Hide the item from the UI

    wordCount -= 1;
    document.getElementById('wordCount').innerText = wordCount;
    sessionStorage.setItem('wordCount', wordCount); // Persist the updated word count
}

function removeWordsFromDOM() {
    if (wordBatchToDelete.length > 0) {
        wordBatchToDelete.forEach(wordId => {
            const wordElement = document.getElementById(`item-${wordId}`);
            if (wordElement) {
                wordElement.style.display = 'none';  // Hide the element immediately
            }
        });
        
        // Update the word count from sessionStorage if available
        const savedWordCount = sessionStorage.getItem('wordCount');
        if (savedWordCount !== null) {
            wordCount = parseInt(savedWordCount);
            document.getElementById('wordCount').innerText = wordCount;
        }
    }
}

function deleteWords() {
    if (wordBatchToDelete.length > 0) {
        const url = '/delete-word';
        const data = JSON.stringify({ wordId: wordBatchToDelete });

        const blob = new Blob([data], { type: 'application/json' });
        const sent = navigator.sendBeacon(url, blob);

        if (!sent) {
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: data,
            }).then(response => {
                if (response.ok) {
                    // Clear the batch after successful deletion
                    wordBatchToDelete = [];
                    sessionStorage.removeItem('wordBatchToDelete');
                } else {
                    console.error('Deletion failed, reloading page might show incorrect data.');
                }
            }).catch(error => {
                console.error('Fallback fetch failed:', error);
            });
        } else {
            // Clear the batch after successful deletion
            wordBatchToDelete = [];
            sessionStorage.removeItem('wordBatchToDelete');
        }
    }
}

// Remove the words from the DOM when the page loads
window.addEventListener('load', removeWordsFromDOM);

// Automatically delete words if there are any in the batch on page load
window.addEventListener('load', deleteWords);



//When pressing 1 - 4 on keayboard, the german characters will be added to the input field (ä, ü, ö, ß)
//Shift + 1 - 4 will add the uppercase version of the characters (Ä, Ü, Ö, ẞ)
document.addEventListener('DOMContentLoaded', (event) => {
    const input = document.getElementById('guess');
    
    // Mapping of keys to custom characters
    const keyMapping = {
        'Digit1': { normal: 'ä', shift: 'Ä' },
        'Digit2': { normal: 'ü', shift: 'Ü' },
        'Digit3': { normal: 'ö', shift: 'Ö' },
        'Digit4': { normal: 'ß', shift: 'ẞ' }
    };

    input.addEventListener('keydown', (e) => {
        // Check if the pressed key is in the keyMapping object
        if (keyMapping.hasOwnProperty(e.code)) {
            e.preventDefault(); // Prevent the default character from being entered

            // Determine if shift key is pressed
            const isShiftPressed = e.shiftKey;

            // Get the current cursor position
            const start = input.selectionStart;
            const end = input.selectionEnd;

            // Get the custom character from the keyMapping
            const customChar = isShiftPressed ? keyMapping[e.code].shift : keyMapping[e.code].normal;
            input.value = input.value.slice(0, start) + customChar + input.value.slice(end);

            // Move the cursor to the correct position after the insertion
            input.setSelectionRange(start + 1, start + 1);
        }
    });
});

//Add german characters to the input field when the buttons are clicked
// Add event listener to each button
document.querySelectorAll('.addChar').forEach(button => {
    button.addEventListener('click', addCharacter);
});

// Add German characters to the input field when the buttons are clicked
function addCharacter(event) {
     // Get the character from the data-char attribute
    let char = event.target.getAttribute('data-char');
        
    // Check if the Shift key is pressed
    if (event.shiftKey) {
        // Convert character to uppercase if possible
        if (char === 'ä') char = 'Ä';
        else if (char === 'ü') char = 'Ü';
        else if (char === 'ö') char = 'Ö';
        else if (char === 'ß') char = 'ẞ';
    }
        
    // Get the input field
    const inputField = document.getElementById('guess');
    // Append the character to the input field's current value
    inputField.value += char;
}

// Event listeners for Shift key press and release + change charaters displayed on buttons to uppercase when Shift key is pressed
document.addEventListener('keydown', handleShiftKey);
document.addEventListener('keyup', handleShiftKey);

function handleShiftKey(event) {
    const isShiftPressed = event.shiftKey;
    document.querySelectorAll('.addChar').forEach(button => {
        let char = button.getAttribute('data-char');
        if (isShiftPressed) {
            if (char === 'ä') button.textContent = 'Ä';
            else if (char === 'ü') button.textContent = 'Ü';
            else if (char === 'ö') button.textContent = 'Ö';
            else if (char === 'ß') button.textContent = 'ẞ';
        } else {
            button.textContent = char;
        }
    });
}

// Attach event listeners to all buttons with the class 'addChar'
const buttons = document.querySelectorAll('.addChar');
buttons.forEach(button => {
    button.addEventListener('click', addCharacter);
});

//Function to focus on the input field when the page loads (mouse stays in the input field after making a word guess)
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("guess").focus();
});

//Function to search for a word
document.getElementById('searchWord').addEventListener('input', function() {
    const searchValue = this.value.toLowerCase();
    const wordItems = document.querySelectorAll('.word-item');
    
    wordItems.forEach(function(item) {
        const englishWord = item.querySelector('.english-word').textContent.toLowerCase();
        const germanWord = item.querySelector('.german-word').textContent.toLowerCase();
        
        if (englishWord.includes(searchValue) || germanWord.includes(searchValue)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});