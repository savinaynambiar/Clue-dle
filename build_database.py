import wikipedia
import json
import re

# Use the same massive list from before
WORDS_TO_PROCESS = [
    "Tiger", "Zebra", "Horse", "Panda", "Eagle", "Shark", "Whale", "Snake", 
    "Sheep", "Camel", "Koala", "Mouse", "Goose", "Moose", "Otter", "Lemur", 
    "Stork", "Heron", "Puppy", "Bison", "Cobra", "Crane", "Crow", "Hyena", 
    "Apple", "Bread", "Pizza", "Sushi", "Fruit", "Grape", "Lemon", "Melon", 
    "Berry", "Onion", "Sugar", "Cream", "Candy", "Steak", "Bacon", "Toast", 
    "Juice", "Sauce", "Pasta", "Salad", "Honey", "Olive", "Peach", "Pecan", 
    "Spice", "Wheat", "Yeast", "Fudge", "Mango", "Basil", "Clove", "Curry",
    "Beach", "River", "Ocean", "Cloud", "Storm", "Grass", "Plant", "Tree", 
    "Stone", "Water", "Flame", "Light", "Night", "Space", "Earth", "World", 
    "Field", "Cliff", "Magma", "Orbit", "Ozone", "Smoke", "Steam", "Swamp",
    "Frost", "Coral", "Delta", "Phone", "Watch", "Clock", "Piano", "Drums", 
    "Flute", "Robot", "Plane", "Train", "Truck", "Motor", "Brick", "Block", 
    "Paper", "Chair", "Table", "Spoon", "Knife", "Plate", "Glass", "Radio", 
    "Video", "Laser", "Radar", "Badge", "Chain", "Fence", "Glove", "Hinge", 
    "Lever", "Pedal", "Scale", "House", "Hotel", "Tower", "Store", "Plaza", 
    "Park", "Yard", "Cabin", "Attic", "Lobby", "Patio", "Ranch", "Shed", 
    "Vault", "Arena", "Depot", "Heart", "Brain", "Mouth", "Tooth", "Blood", 
    "Bones", "Skull", "Chest", "Hands", "Pilot", "Nurse", "Judge", "Guard", 
    "Actor", "Baker", "Clown", "Thief", "Scout", "Ninja", "Chief", "Adult", 
    "Child", "Woman", "Human", "Shirt", "Shoes", "Dress", "Scarf", "Boots", 
    "Cloth", "Denim", "Linen", "Nylon", "Rayon", "Satin", "Silk", "Velvet", 
    "Wool", "Steel", "Metal", "Music", "Dance", "Party", "Dream", "Sleep", 
    "Sound", "Power", "Money", "Color", "Magic", "Ghost", "Alien", "Angel", 
    "Devil", "Fairy", "Giant", "Logic", "Maths", "Peace", "Truth", "Value", 
    "Voice", "Youth", "Error"
]

OUTPUT_FILE = "clues.json"

def clean_sentence(sentence, secret_word):
    """Replaces the secret word with [______]"""
    pattern = re.compile(re.escape(secret_word), re.IGNORECASE)
    cleaned = pattern.sub("[______]", sentence)
    
    # Handle Plurals (e.g. Apple -> Apples)
    if secret_word.endswith('s'):
        singular = secret_word[:-1]
        pattern_sing = re.compile(re.escape(singular), re.IGNORECASE)
        cleaned = pattern_sing.sub("[______]", cleaned)
    else:
        plural = secret_word + "s"
        pattern_plural = re.compile(re.escape(plural), re.IGNORECASE)
        cleaned = pattern_plural.sub("[______]", cleaned)
        
    return cleaned

def fetch_content(word):
    """Smart fetcher that handles errors and short summaries"""
    try:
        # 1. Try to get a longer summary (10 sentences)
        return wikipedia.summary(word, sentences=10, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        # 2. If ambiguous (e.g., Crane bird vs Crane machine), pick the first option
        try:
            print(f"   (Ambiguous: trying '{e.options[0]}')")
            return wikipedia.summary(e.options[0], sentences=10, auto_suggest=False)
        except:
            return ""
    except wikipedia.exceptions.PageError:
        return ""
    except Exception:
        return ""

def build_database():
    database = {}
    print(f"🤖 STARTING SMART BOT... Processing {len(WORDS_TO_PROCESS)} words.")
    
    for i, word in enumerate(WORDS_TO_PROCESS):
        print(f"[{i+1}/{len(WORDS_TO_PROCESS)}] Researching: {word}...", end=" ")
        
        raw_text = fetch_content(word)
        
        if not raw_text:
            print("❌ Failed.")
            continue

        # Split into sentences
        sentences = raw_text.replace('\n', ' ').split('. ')
        
        clean_clues = []
        for s in sentences:
            # Filter bad sentences (too short or too long)
            if len(s) > 20 and len(s) < 300:
                cleaned = clean_sentence(s, word)
                if not cleaned.endswith('.'): cleaned += "."
                
                # Only keep clues where we actually hid the word (ensures relevance)
                if "[______]" in cleaned:
                    clean_clues.append(cleaned)
        
        if len(clean_clues) >= 5:
            # Take first 5 and reverse (Hard -> Easy)
            final_clues = clean_clues[:5]
            final_clues.reverse()
            database[word.upper()] = final_clues
            print(f"✅ Success!")
        else:
            print(f"⚠️ Not enough good clues ({len(clean_clues)} found).")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(database, f, indent=4)
        
    print(f"\n✅ DONE! Saved {len(database)} words to {OUTPUT_FILE}.")

if __name__ == "__main__":
    build_database()