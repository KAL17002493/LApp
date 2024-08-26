//When pressing 1 - 4 on keayboard, the german characters will be added to the input field (ä, ü, ö, ß)
//Shift + 1 - 4 will add the uppercase version of the characters (Ä, Ü, Ö, ẞ)
document.addEventListener('DOMContentLoaded', (event) => {
    const input = document.getElementById('guess');
    
    if (input) {
        const keyMapping = {
            'Digit1': { normal: 'ä', shift: 'Ä' },
            'Digit2': { normal: 'ü', shift: 'Ü' },
            'Digit3': { normal: 'ö', shift: 'Ö' },
            'Digit4': { normal: 'ß', shift: 'ẞ' }
        };

        input.addEventListener('keydown', (e) => {
            if (keyMapping.hasOwnProperty(e.code)) {
                e.preventDefault();

                const isShiftPressed = e.shiftKey;
                const start = input.selectionStart;
                const end = input.selectionEnd;
                const customChar = isShiftPressed ? keyMapping[e.code].shift : keyMapping[e.code].normal;

                input.value = input.value.slice(0, start) + customChar + input.value.slice(end);
                input.setSelectionRange(start + 1, start + 1);
            }
        });

        // Automatically focus the input field
        input.focus();
    }

    // Add event listener to each button to insert German characters
    document.querySelectorAll('.addChar').forEach(button => {
        button.addEventListener('click', (event) => {
            let char = event.target.getAttribute('data-char');
            
            // Check if the Shift key is pressed when the button is clicked
            if (event.shiftKey) {
                if (char === 'ä') char = 'Ä';
                else if (char === 'ü') char = 'Ü';
                else if (char === 'ö') char = 'Ö';
                else if (char === 'ß') char = 'ẞ';
            }

            const inputField = document.getElementById('guess');
            const start = inputField.selectionStart;
            const end = inputField.selectionEnd;

            inputField.value = inputField.value.slice(0, start) + char + inputField.value.slice(end);
            inputField.setSelectionRange(start + char.length, start + char.length);
            inputField.focus();
        });
    });

    // Handle shift key press and release
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
});



//Function to focus on the input field when the page loads (mouse stays in the input field after making a word guess)
document.addEventListener("DOMContentLoaded", function() {
        document.getElementById("guess").focus();
});

//Search for a word
const searchWordErrorRemove = document.getElementById('searchWord'); //Checks if the input field exists on the page (Removes errors fomr devtool screen)
if (searchWordErrorRemove)
{
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
}

//The following code is for the deletion of words!!!
//The following code is for the deletion of words!!!
//The following code is for the deletion of words!!!

//Function to delete a word or list of words
function markForDeletion(wordId)
{
    let wordsToDelete = JSON.parse(sessionStorage.getItem('wordsToDelete')) || [];

    if (!wordsToDelete.includes(wordId)) //Prevents duplicate IDs from being added
    { 
        wordsToDelete.push(wordId);
        sessionStorage.setItem('wordsToDelete', JSON.stringify(wordsToDelete));
        hideItemMarkedForDeletion(wordId);
    }
}

function hideItemMarkedForDeletion(wordId)
{
    //console.log("Hiding word with ID: " + wordId); //Console log to check if the function is working
    const wordItem = document.getElementById(wordId);
    if (sessionStorage.getItem('wordsToDelete').includes(wordId))
    {
        wordItem.style.display = 'none';
    }
}

document.addEventListener("visibilitychange", function()
{
    if (document.visibilityState === 'hidden')
    {
        deleteWords();
    }
});

function deleteWords()
{
    //Parse the words to delete from session storage
    let wordsToDelete = JSON.parse(sessionStorage.getItem('wordsToDelete'));

    if(wordsToDelete !== null) //Runs IF wordsToDelete is not null
    {
        const url = '/delete-word';
        const requestBody = JSON.stringify({ wordsToDelete: wordsToDelete });

        fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: requestBody
        }).then(response => {
            if (response.ok) {
                // Clear the batch after successful deletion
                
            } else {
                console.error('Deletion failed: ' + response.statusText);
            }
        }).catch(error => {
            console.error('Fetch failed:', error);
        });

        sessionStorage.clear("wordsToDelete");
    }
    else
    {
        //No words to delete, so just clear the session storage
        console.log("No words to delete, clearing wordsToDelete from session storage");
    }
}

//Code responsible for the deletion of words ends here!!!
//Code responsible for the deletion of words ends here!!!
//Code responsible for the deletion of words ends here!!!