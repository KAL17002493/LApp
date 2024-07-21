console.log('Hello from main.js');

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
function addCharacter(event) {
    // Get the character from the data-char attribute
    const char = event.target.getAttribute('data-char');
    // Get the input field
    const inputField = document.getElementById('guess');
    // Append the character to the input field's current value
    inputField.value += char;
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

//Function to delete a word
function deleteWord(wordId){
    fetch('/delete-word', {
        method: 'POST',
        body: JSON.stringify({ wordId: wordId }),
    }).then((_res) => {
        window.location.href = '/';
    });
}