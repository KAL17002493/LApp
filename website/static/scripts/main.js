console.log('Hello from main.js');

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