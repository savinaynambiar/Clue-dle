let SECRET_WORD = ""; 
let GAME_CLUES = []; 
const MAX_ATTEMPTS = 5;
let currentAttempt = 0;
let currentGuess = []; 
let gameOver = false;
let validWords = []; 
let winStreak = 0; 

const keysLayout = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];
const board = document.getElementById("game-board");

// UI Elements
const clueLevel = document.getElementById("clue-level");
const clueText = document.getElementById("clue-text");
const restartMenu = document.getElementById("restart-menu");
const streakDisplay = document.getElementById("streak-display");
const keyboardContainer = document.getElementById("keyboard-container");

// --- MAIN FUNCTION TO START/RESTART GAME ---
async function startNewGame() {
    // 1. Hide "Next Level" button
    restartMenu.classList.add("hidden");

    // 2. SHOW KEYBOARD AGAIN (Reset to Flex)
    if(keyboardContainer) keyboardContainer.style.display = "flex";
    
    // Reset UI Texts
    // showToast("Loading Riddle..."); // REMOVED as requested
    
    // Reset Clue Box Style
    const clueBox = document.querySelector(".clue-box");
    clueBox.classList.remove("game-over-state");
    clueLevel.style.color = "#818384";
    clueLevel.style.background = "#121213";
    
    // Default text
    document.getElementById("clue-text").textContent = "Loading riddle...";

    try {
        // Fetch JSON directly
        const response = await fetch('clues.json');
        const allData = await response.json();
        
        // Pick a random word
        const words = Object.keys(allData);
        SECRET_WORD = words[Math.floor(Math.random() * words.length)];
        GAME_CLUES = allData[SECRET_WORD];

        console.log("Game Loaded."); 
        
        // Load dictionary only if empty
        if (validWords.length === 0) await loadDictionary();

        resetBoard(); 
        createKeyboard();
        
    } catch (error) {
        console.error(error);
        showToast("Error loading game data.");
    }
}

async function loadDictionary() {
    try {
        const response = await fetch('words.txt');
        if (!response.ok) throw new Error("File not found");
        const text = await response.text();
        validWords = text.split('\n').map(w => w.trim().toUpperCase()).filter(w => w.length === 5);
        console.log("Dictionary loaded:", validWords.length);
    } catch (error) { 
        console.error("Error loading words.txt:", error);
    }
}

function createKeyboard() {
    document.getElementById("row-1").innerHTML = "";
    document.getElementById("row-2").innerHTML = "";
    document.getElementById("row-3").innerHTML = "";

    const makeKey = (letter, rowId, isWide = false) => {
        let btn = document.createElement("div");
        btn.textContent = letter;
        btn.classList.add("key");
        if (isWide) btn.classList.add("wide-key");
        btn.id = "key-" + letter; 
        
        btn.addEventListener("click", () => {
            if (letter === "ENTER") checkGuess();
            else if (letter === "⌫") deleteLetter();
            else addLetter(letter);
        });
        document.getElementById(rowId).appendChild(btn);
    };

    keysLayout[0].split("").forEach(k => makeKey(k, "row-1"));
    keysLayout[1].split("").forEach(k => makeKey(k, "row-2"));
    makeKey("ENTER", "row-3", true);
    keysLayout[2].split("").forEach(k => makeKey(k, "row-3"));
    makeKey("⌫", "row-3", true);
}

function resetBoard() {
    currentAttempt = 0;
    currentGuess = [];
    gameOver = false;
    board.innerHTML = "";
    
    clueLevel.textContent = "1";
    clueText.textContent = GAME_CLUES[0];

    board.style.gridTemplateColumns = `repeat(${SECRET_WORD.length}, 1fr)`;
    for (let i = 0; i < MAX_ATTEMPTS * SECRET_WORD.length; i++) {
        let tile = document.createElement("div");
        tile.classList.add("tile");
        tile.id = "tile-" + i;
        board.appendChild(tile);
    }
}

document.addEventListener("keydown", (e) => {
    if (!restartMenu.classList.contains("hidden") && e.key === "Enter") {
        startNewGame();
        return;
    }
    if (gameOver || !SECRET_WORD) return;
    let key = e.key.toUpperCase();
    if (key === "ENTER") checkGuess();
    else if (key === "BACKSPACE") deleteLetter();
    else if (isLetter(key)) addLetter(key);
});

function isLetter(str) { return str.length === 1 && str.match(/[A-Z]/i); }

function addLetter(letter) {
    if (currentGuess.length < SECRET_WORD.length) {
        currentGuess.push(letter);
        let rowStart = currentAttempt * SECRET_WORD.length;
        let tile = document.getElementById(`tile-${rowStart + currentGuess.length - 1}`);
        tile.textContent = letter;
        tile.classList.add("pop");
        tile.style.borderColor = "#818384"; 
    }
}

function deleteLetter() {
    if (currentGuess.length > 0) {
        let rowStart = currentAttempt * SECRET_WORD.length;
        let tile = document.getElementById(`tile-${rowStart + currentGuess.length - 1}`);
        tile.textContent = "";
        tile.classList.remove("pop");
        tile.style.borderColor = "#3a3a3c"; 
        currentGuess.pop();
    }
}

function checkGuess() {
    if (currentGuess.length !== SECRET_WORD.length) {
        shakeBoard();
        return;
    }

    let guessString = currentGuess.join("");
    
    // Dictionary Check
    if (validWords.length > 0 && !validWords.includes(guessString)) {
        shakeBoard(); 
        // Toast hidden as requested
        return;
    }

    let isCorrect = (guessString === SECRET_WORD);
    let rowStart = currentAttempt * SECRET_WORD.length;
    let letterCounts = {};
    for (let char of SECRET_WORD) letterCounts[char] = (letterCounts[char] || 0) + 1;
    let guessColors = new Array(SECRET_WORD.length).fill("absent");

    // Pass 1: Green
    for (let i = 0; i < SECRET_WORD.length; i++) {
        if (currentGuess[i] === SECRET_WORD[i]) {
            guessColors[i] = "correct";
            letterCounts[currentGuess[i]]--;
        }
    }
    // Pass 2: Yellow
    for (let i = 0; i < SECRET_WORD.length; i++) {
        if (guessColors[i] === "absent") { 
            let letter = currentGuess[i];
            if (letterCounts[letter] > 0) {
                guessColors[i] = "present";
                letterCounts[letter]--;
            }
        }
    }

    // ANIMATION LOOP
    for (let i = 0; i < SECRET_WORD.length; i++) {
        let tile = document.getElementById(`tile-${rowStart + i}`);
        let letter = currentGuess[i];
        let keyBtn = document.getElementById("key-" + letter);
        let status = guessColors[i];

        setTimeout(() => {
            tile.classList.add("flip");
            setTimeout(() => {
                tile.classList.add(status);
                tile.classList.remove("pop");
                tile.style.borderColor = "transparent"; 
                if (keyBtn) {
                    if (status === "correct") {
                        keyBtn.classList.remove("present", "absent"); keyBtn.classList.add("correct");
                    } else if (status === "present" && !keyBtn.classList.contains("correct")) {
                        keyBtn.classList.add("present");
                    } else if (status === "absent" && !keyBtn.classList.contains("correct") && !keyBtn.classList.contains("present")) {
                        keyBtn.classList.add("absent");
                    }
                }
            }, 300); 
        }, i * 250); 
    }

    // GAME END LOGIC
    setTimeout(() => {
        if (isCorrect) {
            showToast("🌟 SPLENDID! 🌟");
            winStreak++;
            showRestartButton(); 
            for(let i=0; i<SECRET_WORD.length; i++){
                setTimeout(()=>{
                    document.getElementById(`tile-${rowStart + i}`).classList.add("win-bounce");
                }, i * 100);
            }
            gameOver = true;
        } else {
            currentAttempt++;
            currentGuess = [];
            if (currentAttempt >= MAX_ATTEMPTS) {
                winStreak = 0; 
                const clueBox = document.querySelector(".clue-box");
                clueBox.classList.add("game-over-state");
                clueLevel.textContent = "GAME OVER";
                clueLevel.style.color = "#d13030"; 
                clueLevel.style.background = "rgba(0,0,0,0.3)";
                clueText.innerHTML = `THE WORD WAS:<br><span class="reveal-word">${SECRET_WORD}</span>`;
                showRestartButton();
                gameOver = true;
            } else {
                if (currentAttempt < GAME_CLUES.length) {
                    clueLevel.textContent = currentAttempt + 1;
                    clueText.textContent = GAME_CLUES[currentAttempt];
                    showToast("New Clue Unlocked!");
                }
            }
        }
    }, (SECRET_WORD.length * 250) + 500); 
}

function showRestartButton() {
    streakDisplay.textContent = "Streak: " + winStreak;
    restartMenu.classList.remove("hidden");
    // HIDE KEYBOARD
    if(keyboardContainer) keyboardContainer.style.display = "none";
}

function showToast(message) {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.classList.add("toast");
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = "0"; setTimeout(() => container.removeChild(toast), 500); }, 2000);
}

function shakeBoard() {
    let rowStart = currentAttempt * SECRET_WORD.length;
    for (let i = 0; i < SECRET_WORD.length; i++) {
        let tile = document.getElementById(`tile-${rowStart + i}`);
        tile.classList.remove("pop"); 
        tile.classList.remove("shake");
        void tile.offsetWidth; 
        tile.classList.add("shake");
        setTimeout(() => tile.classList.remove("shake"), 500);
    }
}

// HELP MODAL TOGGLE
function toggleHelp() {
    const modal = document.getElementById("help-modal");
    if (modal.classList.contains("hidden")) {
        modal.classList.remove("hidden");
    } else {
        modal.classList.add("hidden");
    }
}

// Start first game
startNewGame();