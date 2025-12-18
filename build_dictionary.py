import requests

def build_dictionary():
    print("📚 Downloading official 5-letter word list...")
    
    # This is the standard list of valid Wordle guesses
    url = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
    
    try:
        r = requests.get(url)
        # Convert to Uppercase and split
        words = r.text.upper().splitlines()
        
        # Double check we only get 5-letter words
        fives = [w.strip() for w in words if len(w.strip()) == 5]
        
        with open("words.txt", "w") as f:
            f.write("\n".join(fives))
            
        print(f"✅ Success! Saved {len(fives)} valid words to words.txt")
        print("   You can now restart your server.")
        
    except Exception as e:
        print(f"❌ Error downloading: {e}")

if __name__ == "__main__":
    build_dictionary()