// Word collections
const wordCollections = {
    nouns: ['cat', 'dog', 'teacher', 'neighbor', 'country', 'computer', 'book', 'student', 'car', 'house', 
            'phone', 'flower', 'mountain', 'ocean', 'friend', 'family', 'city', 'artist', 'doctor', 'child'],
    verbs: ['runs', 'jumps', 'speaks', 'writes', 'reads', 'drives', 'sleeps', 'eats', 'works', 'plays',
            'sings', 'dances', 'swims', 'teaches', 'learns', 'grows', 'builds', 'creates', 'helps', 'loves'],
    adjectives: ['happy', 'sad', 'big', 'small', 'beautiful', 'smart', 'funny', 'serious', 'old', 'new',
                'quiet', 'loud', 'bright', 'dark', 'strong', 'weak', 'rich', 'poor', 'hot', 'cold'],
    adverbs: ['quickly', 'slowly', 'carefully', 'loudly', 'quietly', 'easily', 'happily', 'always', 'never', 'sometimes',
              'rarely', 'often', 'extremely', 'barely', 'nearly', 'almost', 'surely', 'possibly', 'gracefully', 'awkwardly'],
    conjunctions: ['and', 'but', 'or', 'because', 'so', 'while', 'although', 'since', 'unless', 'until',
                  'if', 'though', 'whereas', 'whether', 'as', 'after', 'before', 'when', 'whenever', 'where'],
    prepositions: ['in', 'on', 'at', 'with', 'by', 'for', 'from', 'of', 'to', 'about',
                  'under', 'over', 'through', 'between', 'among', 'around', 'behind', 'beyond', 'during', 'without'],
    articles: ['a', 'an', 'the']
};

// DOM Elements
const generatedSentence = document.getElementById('generatedSentence');
const sentenceEditor = document.getElementById('sentenceEditor');
const editorSection = document.getElementById('editorSection');
const wordCollectionsContainer = document.getElementById('wordCollections');
const generateBtn = document.getElementById('generateBtn');
const editBtn = document.getElementById('editBtn');
const saveBtn = document.getElementById('saveBtn');
const cancelBtn = document.getElementById('cancelBtn');
const toggleWordsBtn = document.getElementById('toggleWordsBtn');

// Current sentence
let currentSentence = '';

// Initialize word collections display
function initializeWordCollections() {
    wordCollectionsContainer.innerHTML = '';
    
    Object.entries(wordCollections).forEach(([category, words]) => {
        const collectionElement = document.createElement('div');
        collectionElement.className = 'word-collection';
        
        const titleElement = document.createElement('h3');
        titleElement.className = 'collection-title';
        titleElement.textContent = category.charAt(0).toUpperCase() + category.slice(1);
        
        const chipsContainer = document.createElement('div');
        chipsContainer.className = 'word-chips';
        
        words.forEach(word => {
            const chip = document.createElement('span');
            chip.className = 'word-chip';
            chip.textContent = word;
            chip.addEventListener('click', () => {
                if (!editorSection.classList.contains('hidden')) {
                    insertWordAtCursor(word);
                }
            });
            chipsContainer.appendChild(chip);
        });
        
        collectionElement.appendChild(titleElement);
        collectionElement.appendChild(chipsContainer);
        wordCollectionsContainer.appendChild(collectionElement);
    });
}

// Generate a random sentence
function generateRandomSentence() {
    const getRandomWord = (category) => {
        const words = wordCollections[category];
        return words[Math.floor(Math.random() * words.length)];
    };
    
    // Simple pattern: Article + Adjective + Noun + Verb + Adverb
    const article = getRandomWord('articles');
    const adjective = getRandomWord('adjectives');
    const noun = getRandomWord('nouns');
    const verb = getRandomWord('verbs');
    const adverb = getRandomWord('adverbs');
    
    let sentence = '';
    
    // 50% chance of adding a second part to the sentence
    if (Math.random() > 0.5) {
        const conjunction = getRandomWord('conjunctions');
        const article2 = getRandomWord('articles');
        const adjective2 = getRandomWord('adjectives');
        const noun2 = getRandomWord('nouns');
        
        sentence = `${article} ${adjective} ${noun} ${verb} ${adverb}, ${conjunction} ${article2} ${adjective2} ${noun2}.`;
    } else {
        const preposition = getRandomWord('prepositions');
        const article2 = getRandomWord('articles');
        const noun2 = getRandomWord('nouns');
        
        sentence = `${article} ${adjective} ${noun} ${verb} ${adverb} ${preposition} ${article2} ${noun2}.`;
    }
    
    // Capitalize first letter
    return sentence.charAt(0).toUpperCase() + sentence.slice(1);
}

// Insert a word at the cursor position in the editor
function insertWordAtCursor(word) {
    const startPos = sentenceEditor.selectionStart;
    const endPos = sentenceEditor.selectionEnd;
    const text = sentenceEditor.value;
    const before = text.substring(0, startPos);
    const after = text.substring(endPos);
    
    // Add space if needed
    let insertText = word;
    if (startPos > 0 && before.slice(-1) !== ' ' && before.slice(-1) !== '\n') {
        insertText = ' ' + insertText;
    }
    
    // Add space after if needed
    if (endPos < text.length && after.charAt(0) !== ' ' && after.charAt(0) !== '\n') {
        insertText = insertText + ' ';
    }
    
    sentenceEditor.value = before + insertText + after;
    
    // Set new cursor position
    const newCursorPos = startPos + insertText.length;
    sentenceEditor.focus();
    sentenceEditor.setSelectionRange(newCursorPos, newCursorPos);
}

// Event Listeners
generateBtn.addEventListener('click', () => {
    currentSentence = generateRandomSentence();
    generatedSentence.textContent = currentSentence;
});

editBtn.addEventListener('click', () => {
    if (currentSentence) {
        sentenceEditor.value = currentSentence;
        editorSection.classList.remove('hidden');
    } else {
        alert('Please generate a sentence first!');
    }
});

saveBtn.addEventListener('click', () => {
    currentSentence = sentenceEditor.value;
    generatedSentence.textContent = currentSentence;
    editorSection.classList.add('hidden');
});

cancelBtn.addEventListener('click', () => {
    editorSection.classList.add('hidden');
});

toggleWordsBtn.addEventListener('click', () => {
    if (wordCollectionsContainer.style.display === 'none') {
        wordCollectionsContainer.style.display = 'grid';
        toggleWordsBtn.textContent = 'Hide';
    } else {
        wordCollectionsContainer.style.display = 'none';
        toggleWordsBtn.textContent = 'Show';
    }
});

// Initialize
initializeWordCollections();