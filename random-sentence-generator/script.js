// Word collections
// const wordCollections = {
//     nouns: ['Maderchod', 'Bhosadike', 'Bhen', 'Beti', 'Bhadhava',  'Chutiya', 'Gaand', 'Gaandu', 'Gadha', 'Lauda', 'Hijra', 'Kuttiya', 'Paad', 'Randi', 'Saala', 'Saali', 'Tatti', 
//         'Kamina', 'Chut', 'Choot', 'Chipkali', 
//         'Chinaal', 'Chullu', 'Cuntmama', 'Chhed', 'Apni', 'Bhosdi-Wala','Bhosdina', 'Bhadwa','Batak','Bakri', 'Buddha', 'Chunni', 'Chinaar',  'Chudan', 'Chut', 'Gaand', 'Jhat',
//          'Chutda', 'Kadak', 'Kali', 'Khotey', 'Kutte', 'Lavde', 'Lund', 'Meri', 'Moot', 'Najayaz', 'Rundi', 'Sadi', 'Teri', 'Tere', 'Ullu'],

//     verbs: ['Chodu','Chudai','runs', 'jumps', 'speaks', 'writes', 'reads', 'drives', 'sleeps', 'eats', 'works', 'plays',
//             'sings', 'dances', 'swims', 'teaches', 'learns', 'grows', 'builds', 'creates', 'helps', 'loves'],
//     adjectives: ['happy', 'sad', 'big', 'small', 'beautiful', 'smart', 'funny', 'serious', 'old', 'new',
//                 'quiet', 'loud', 'bright', 'dark', 'strong', 'weak', 'rich', 'poor', 'hot', 'cold'],
//     adverbs: ['quickly', 'slowly', 'carefully', 'loudly', 'quietly', 'easily', 'happily', 'always', 'never', 'sometimes',
//               'rarely', 'often', 'extremely', 'barely', 'nearly', 'almost', 'surely', 'possibly', 'gracefully', 'awkwardly'],
//     conjunctions: ['and', 'but', 'or', 'because', 'so', 'while', 'although', 'since', 'unless', 'until',
//                   'if', 'though', 'whereas', 'whether', 'as', 'after', 'before', 'when', 'whenever', 'where'],
//     prepositions: ['in', 'on', 'at', 'with', 'by', 'for', 'from', 'of', 'to', 'about',
//                   'under', 'over', 'through', 'between', 'among', 'around', 'behind', 'beyond', 'during', 'without'],
//     articles: ['a', 'an', 'the']
// };

const wordCollections = {
    nouns: ['Maderchod', 'Bhosadike','Bhos','Pikko', 'Bhen', 'Beti', 'Bhadhava', 'Chutiya', 'Gaand', 'Gaandu', 'Gadha', 'Lauda', 'Hijra', 'Kuttiya', 'Paad', 'Randi', 'Saala', 'Saali', 'Tatti', 
            'Kamina', 'Chut', 'Choot', 'Chipkali', 'Chinaal', 'Chullu', 'Cuntmama', 'Chhed', 'Apni', 'Bhosdi-Wala', 'Bhosdina', 'Bhadwa', 'Batak', 'Bakri', 'Buddha', 'Chunni', 
            'Chinaar','Bailaa', 'Chutda', 'Kadak', 'Kali', 'Khotey', 'Kutte', 'Lavde', 'Lund', 'Meri', 'Moot', 'Najayaz', 'Rundi', 'Sadi', 'Teri', 'Tere', 'Ullu', 'Jhaant', 'Hazaar'],

    verbs: ['Chodu', 'Chudai', 'Chus', 'Mar', 'Pel', 'Bajaa', 'Thok', 'Chhap', 'Ghusaa', 'Nikal', 
            'Dha', 'Fek', 'Gandh', 'Jhank', 'Tadpa', 'Rula', 'Sata', 'Jala', 'Chhina', 'Lut', 'Bhaag', 'Kha'],

    adjectives: ['Ganda','Chmakti', 'Sada', 'Bada', 'Chhota', 'Chutiya', 'Bakwas', 'Ghatia', 'Tuchh', 'Buddha', 'Naya',
                 'Chup', 'Bajau', 'Chamkila', 'Kaala', 'Tagda', 'Kamzor', 'Ameer', 'Gareeb', 'Tapta', 'Thanda'],

    adverbs: ['Jaldi', 'Dheere', 'Dhyaan', 'Zor', 'Chupke', 'Aasani', 'Khushi', 'Hamesha', 'Kabhi', 'Kabhi-Kabhi',
              'Kam', 'Aksar', 'Bohot', 'Thoda', 'Lagbhag', 'Haan', 'Shayad', 'Sundar', 'Bekaari'],

    conjunctions: ['Aur', 'Par', 'Ya', 'Kyuki', 'Toh', 'Jab', 'Hala', 'Se', 'Nahi', 'Tak',
                   'Agar', 'Firbhi', 'Jahan', 'Kya', 'Jaise', 'Baad', 'Pehle', 'Kab', 'Jabhi', 'Jaha'],
    
    
    // prepositions: ['Mein', 'Par', 'Pe', 'Saath', 'Se', 'Ke', 'Se', 'Ka', 'Ko', 'Bout',
    //                'Neeche', 'Upar', 'Ke', 'Beech', 'Saath', 'Charo', 'Piche', 'Aage', 'Dauran', 'Bina'],
    
    articles: ['Ek', 'Woh', 'Yeh','Tari','Eni','Ena']
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
// Generate a random sentence - optimized for speed
function generateRandomSentence() {
    // Fast random word selection with bitwise operations for better performance
    const getRandomWord = (category) => {
        try {
            const words = wordCollections[category];
            const index = (Math.random() * words.length) | 0; // Bitwise OR for faster integer conversion
            return words[index];
        } catch (error) {
            // Fallback for missing categories
            return '';
        }
    };
    
    // Pre-fetch words once to avoid multiple lookups
    const article = getRandomWord('articles');
    const adjective = getRandomWord('adjectives');
    const noun = getRandomWord('nouns');
    const verb = getRandomWord('verbs');
    const adverb = getRandomWord('adverbs');
    
    // Use simple string concatenation for better performance
    let sentence = article + ' ' + adjective + ' ' + noun + ' ' + verb + ' ' + adverb;
    
    // Simpler fallback - always use conjunctions instead of prepositions
    if (Math.random() < 0.5) {
        const conjunction = getRandomWord('conjunctions');
        const article2 = getRandomWord('articles');
        const adjective2 = getRandomWord('adjectives');
        const noun2 = getRandomWord('nouns');
        
        sentence += ', ' + conjunction + ' ' + article2 + ' ' + adjective2 + ' ' + noun2;
    }
    
    // Add period at the end
    sentence += '.';
    
    // Capitalize first letter efficiently
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

// Event Listeners - optimized for performance
generateBtn.addEventListener('click', () => {
    // Add loading indication
    generatedSentence.textContent = "Generating...";
    
    // Use setTimeout to prevent UI freezing
    setTimeout(() => {
        currentSentence = generateRandomSentence();
        generatedSentence.textContent = currentSentence;
    }, 0);
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

const readyMadeSentences = [
  "Tane akkal no tukko nathi!",
  "Chutiya, tari gaand ma dandiyo ramto che!",
  "Saala, tu toh khotey no khoto che!",
  "Bhadwa, tari buddhi ma budbud thay che!",
  "Ullu no paththo, kya thi aavyo che tu?",
  "Taro dimag toh fokat no fuse che!",
  "Ghaamdi, tu toh vahiyaat no vahan che!",
  "Dheela chhokro, kya ma fafdo kare che!",
  "Tari buddhi toh bhaangar ni peti che!",
  "Saali chipkali, jya jaye tya lapetay!",
  "Teri akal ka tala khula nahi!",
  "Chutiya, kyun ban ke ghum raha hai?",
  "Saale, tu toh ullu ka pattha hai!",
  "Gadhe ke peeche gadha, tu sabse bada!",
  "Bhosdike, dimag mein tatti bhari hai kya?",
  "Kameena, tera fuse ud gaya kya!",
  "Fuddu, tu toh faltu ka fafda hai!",
  "Bewakoof, teri buddhi mein jhaant bhar gayi!",
  "Tera dimag toh nakli ka naatak che!",
  "Pagalpan ki dukaan, tu hi hai uska maalik!",
  "Taro maa no bhosdo, kya thi tu paida thayo!",
  "Saala bhadwa, tari gaand ma dandiyo ghusadu!",
  "Chutiya lavde, taren dimag ma tatti no dago!",
  "Randi no chhokro, tu toh gandh ni naali che!",
  "Teri ben no lundo, kya ma tu hagto jaye che!",
  "Bhosdi na, tari buddhi toh moot ma dubi che!",
  "Khotey na khota, taren muh ma paad maru!",
  "Tari maa ni chut ma dhamakedar bomb!",
  "Saali kuttiya, taren ghar ma jhaant no jhado!",
  "Taro baap no lauda, tu toh najayaz aulaad che!",
  "Teri maa ka bhosda, tu kahan se paida hua!",
  "Saale bhadwe, teri gaand mein danda daal doon!",
  "Chutiye laude, tere dimaag mein tatti bhari hai!",
  "Randi ka baccha, tu toh gandi naali ka keeda hai!",
  "Teri behen ka lund, tu kahan se bhaag ke aaya!",
  "Bhosdike, tera dimaag moot mein doob gaya!",
  "Khotey ka khota, tere muh mein paad maroon!",
  "Teri maa ki chut mein pataka phod doon!",
  "Saali kutti, tere ghar mein jhaant ka jungle!",
  "Tera baap ka lauda, tu toh harami aulaad hai!"
];
// Ready-made sentences section

    /*
   "Tane akkal no tukko nathi!
Chutiyo, tari gaand ma dandiyo ramto che!
Saala, tu toh khotey no khoto che!
Bhadwa, tari buddhi ma budbud thay che!
Ullu no paththo, kya thi aavyo che tu?
Taro dimag toh fokat no fuse che!
Ghaamdi, tu toh vahiyaat no vahan che!
Dheela chhokro, kya ma fafdo kare che!
Tari buddhi toh bhaangar ni peti che!
Saali chipkali, jya jaye tya lapetay!
and Teri akal ka tala khula nahi!
Chutiya, kyun ban ke ghum raha hai?
Saale, tu toh ullu ka pattha hai!
Gadhe ke peeche gadha, tu sabse bada!
Bhosdike, dimag mein tatti bhari hai kya?
Kameena, tera fuse ud gaya kya!
Fuddu, tu toh faltu ka fafda hai!
Bewakoof, teri buddhi mein jhaant bhar gayi!
Tera dimag toh nakli ka naatak che!
Pagalpan ki dukaan, tu hi hai uska maalik!
also add Taro maa no bhosdo, kya thi tu paida thayo!
Saala bhadwa, tari gaand ma dandiyo ghusadu!
Chutiya lavde, taren dimag ma tatti no dago!
Randi no chhokro, tu toh gandh ni naali che!
Teri ben no lundo, kya ma tu hagto jaye che!
Bhosdi na, tari buddhi toh moot ma dubi che!
Khotey na khota, taren muh ma paad maru!
Tari maa ni chut ma dhamakedar bomb!
Saali kuttiya, taren ghar ma jhaant no jhado!
Taro baap no lauda, tu toh najayaz aulaad che!
Teri maa ka bhosda, tu kahan se paida hua!
Saale bhadwe, teri gaand mein danda daal doon!
Chutiye laude, tere dimaag mein tatti bhari hai!
Randi ka baccha, tu toh gandi naali ka keeda hai!
Teri behen ka lund, tu kahan se bhaag ke aaya!
Bhosdike, tera dimaag moot mein doob gaya!
Khotey ka khota, tere muh mein paad maroon!
Teri maa ki chut mein pataka phod doon!
Saali kutti, tere ghar mein jhaant ka jungle!
Tera baap ka lauda, tu toh harami aulaad hai!
    */
// Initialize ready-made sentences display

function initializeReadyMadeSentences() {
  const readyMadeSection = document.getElementById('readyMadeSection');
  
  readyMadeSentences.forEach(sentence => {
    const sentenceCard = document.createElement('div');
    sentenceCard.className = 'sentence-card';
    
    const sentenceText = document.createElement('p');
    sentenceText.textContent = sentence;
    
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-btn';
    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
    copyButton.setAttribute('data-tooltip', 'Copy to clipboard');
    
    copyButton.addEventListener('click', () => {
      navigator.clipboard.writeText(sentence)
        .then(() => {
          // Show copied feedback
          copyButton.classList.add('copied');
          copyButton.setAttribute('data-tooltip', 'Copied!');
          
          setTimeout(() => {
            copyButton.classList.remove('copied');
            copyButton.setAttribute('data-tooltip', 'Copy to clipboard');
          }, 2000);
        })
        .catch(err => {
          console.error('Failed to copy: ', err);
        });
    });
    
    // Use button for selecting ready-made sentence
    const useButton = document.createElement('button');
    useButton.className = 'use-btn';
    useButton.textContent = 'Use';
    useButton.addEventListener('click', () => {
      currentSentence = sentence;
      generatedSentence.textContent = currentSentence;
      
      // Scroll to sentence section
      document.querySelector('.sentence-display').scrollIntoView({
        behavior: 'smooth'
      });
    });
    
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'button-container';
    buttonContainer.appendChild(copyButton);
    buttonContainer.appendChild(useButton);
    
    sentenceCard.appendChild(sentenceText);
    sentenceCard.appendChild(buttonContainer);
    readyMadeSection.appendChild(sentenceCard);
  });
}

// Toggle ready-made sentences section
const toggleReadyMadeBtn = document.getElementById('toggleReadyMadeBtn');
const readyMadeContainer = document.getElementById('readyMadeContainer');

toggleReadyMadeBtn.addEventListener('click', () => {
  if (readyMadeContainer.style.display === 'none' || !readyMadeContainer.style.display) {
    readyMadeContainer.style.display = 'block';
    toggleReadyMadeBtn.textContent = 'Hide Ready-Made Sentences';
  } else {
    readyMadeContainer.style.display = 'none';
    toggleReadyMadeBtn.textContent = 'Show Ready-Made Sentences';
  }
});

// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  const isDarkMode = document.body.classList.contains('dark-mode');
  darkModeToggle.innerHTML = isDarkMode ? 
    '<i class="fas fa-sun"></i>' : 
    '<i class="fas fa-moon"></i>';
  
  // Save preference
  localStorage.setItem('darkMode', isDarkMode);
});

// Check for saved dark mode preference
document.addEventListener('DOMContentLoaded', () => {
  const savedDarkMode = localStorage.getItem('darkMode') === 'true';
  if (savedDarkMode) {
    document.body.classList.add('dark-mode');
    darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  }
});

// Initialize existing collections and ready-made sentences
initializeWordCollections();
initializeReadyMadeSentences();