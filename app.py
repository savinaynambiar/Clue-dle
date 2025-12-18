import random
import json
import os
from flask import Flask, jsonify, send_from_directory

# Try to import livereload for auto-refreshing
try:
    from livereload import Server
    HAS_LIVERELOAD = True
except ImportError:
    HAS_LIVERELOAD = False
    print("⚠️  livereload not installed. Run 'pip install livereload' for auto-refresh.")

app = Flask(__name__, static_url_path='', static_folder='.')

# CONFIGURATION
DB_FILE = "clues.json"
GAME_DATA = {}

def load_database():
    """Loads the massive clue list from the JSON file"""
    global GAME_DATA
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            GAME_DATA = json.load(f)
        print(f"Server: Loaded {len(GAME_DATA)} words from database.")
    else:
        print("Server: Error! clues.json not found. Run build_database.py first!")
        GAME_DATA = {
            "ERROR": ["Run build_database.py", "File Missing", "Check Terminal", "No Data", "System Error"]
        }

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/new-game')
def new_game():
    if not GAME_DATA:
        load_database()
        
    if not GAME_DATA:
        return jsonify({"error": "No data"}), 500
        
    secret_word = random.choice(list(GAME_DATA.keys()))
    clues = GAME_DATA[secret_word]
    
    print(f"Server: New game is {secret_word}")
    
    return jsonify({
        "word": secret_word,
        "clues": clues
    })

if __name__ == '__main__':
    load_database()
    
    if HAS_LIVERELOAD:
        print("🟢 LIVE SERVER ACTIVE! Saving files will refresh the browser.")
        server = Server(app.wsgi_app)
        server.watch('index.html')
        server.watch('style.css')
        server.watch('script.js')
        # Using port 5000. If it fails, change to 5001.
        server.serve(port=5000, open_url_delay=1)
    else:
        print("STARTING STANDARD SERVER...")
        app.run(debug=True, port=5001)