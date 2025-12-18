# 🧩 Clue-dle: The Daily Riddle Word Game

**Clue-dle** is a twist on the classic word-guessing genre. Instead of guessing blindly, players must use lateral thinking to solve a cryptic riddle that guides them to the secret 5-letter word.

![Game Screenshot](image_af229a.png) 
*(Replace the above text with a link to your actual screenshot after uploading)*

## 🚀 Live Demo
**Play the game here:** [INSERT YOUR NETLIFY/GITHUB LINK HERE]

---

## ✨ Features

* **Riddle-Based Gameplay:** Every level starts with a unique clue from a database of thousands of words.
* **Endless Mode:** Play as many levels as you want. The game instantly fetches a new riddle upon winning.
* **Win Streak Tracker:** Keeps track of consecutive wins to challenge players.
* **Juicy Animations:**
    * Tile "Pop" on entry.
    * Board "Shake" on invalid words.
    * Card "Flip" reveal sequence.
    * Winning "Bounce" celebration.
* **Responsive Design:** Fully optimized for Desktop and Mobile (Auto-hiding keyboard on win).
* **Lightweight & Static:** No backend server required. Runs entirely in the browser using JSON.

---

## 🎮 How to Play

1.  **Read the Clue:** Look at the riddle at the top of the screen (e.g., *"A space at the top of a house"*).
2.  **Guess the Word:** Type a 5-letter word that fits the clue (e.g., `ATTIC`).
3.  **Check the Colors:**
    * 🟩 **Green:** Correct letter in the correct spot.
    * 🟨 **Yellow:** Correct letter but in the wrong spot.
    * ⬛ **Gray:** The letter is not in the word.
4.  **Win:** Guess the word within 5 attempts to increase your streak!

---

## 🛠️ Installation & Setup

Since this game is **Static** (HTML/CSS/JS), you don't need to install Node.js or Python to run it.

### Option 1: VS Code (Recommended)
1.  Clone or download this repository.
2.  Open the folder in **VS Code**.
3.  Install the **"Live Server"** extension.
4.  Right-click `index.html` and select **"Open with Live Server"**.

### Option 2: Basic Browser
1.  Simply double-click `index.html` to open it in your browser.
    * *Note: Some browsers block `fetch()` requests for JSON files when opening locally. If the game gets stuck on "Loading...", use Option 1.*

---

## 📂 Project Structure

```text
/Clue-dle
│
├── index.html       # The main game structure and SEO tags
├── style.css        # Game styling, animations, and modal layout
├── script.js        # Game logic (Word validation, coloring, state management)
├── clues.json       # Database of words and their associated riddles
├── words.txt        # Dictionary file for validating user guesses
├── logo.png         # Game icon/Favicon
└── README.md        # This file