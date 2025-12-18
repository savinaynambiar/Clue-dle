import cv2
import os
import random
import requests
import numpy as np
from duckduckgo_search import DDGS

# CONFIGURATION
OUTPUT_DIR = "assets"

WORD_LIST = [
    "GUITAR", "CASTLE", "FOREST", "PLANET", "JUNGLE", 
    "DESERT", "BRIDGE", "ISLAND", "CANYON", "WINDOW", 
    "MARKET", "OFFICE", "TEMPLE", "STATUE", "ROCKET", 
    "TURTLE", "DOLPHIN", "PIRATE", "GARDEN", "TUNNEL",
    "VOLCANO", "SUMMER", "WINTER", "AUTUMN", "SPRING",
    "BANANA", "ORANGE", "CHERRY", "BUTTER", "CHEESE",
    "DINNER", "LUNCH", "BRUNCH", "PICNIC", "PENCIL",
    "BOTTLE", "LAPTOP", "CAMERA", "JACKET", "HELMET",
    "BUTTON", "POCKET", "SCHOOL", "CIRCUS", "PARADE"
]

def search_image_url(word):
    """Searches DuckDuckGo for the word and returns the first image URL."""
    print(f"🔍 Searching DuckDuckGo for: {word}...")
    try:
        with DDGS() as ddgs:
            # Search for the word, get 1 result
            results = list(ddgs.images(word, max_results=1))
            if results:
                image_url = results[0]['image']
                print(f"   Found URL: {image_url}")
                return image_url
            else:
                print("   No results found.")
                return None
    except Exception as e:
        print(f"   Search failed: {e}")
        return None

def download_image(url):
    """Downloads the image from the specific URL found."""
    print("⬇️  Downloading image...")
    
    # We need a 'User-Agent' so websites think we are a real browser, not a bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            image_array = np.asarray(bytearray(response.content), dtype="uint8")
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print(f"   Failed to download (Status: {response.status_code})")
            return None
    except Exception as e:
        print(f"   Download error: {e}")
        return None

def pixelate_image(image, pixel_size):
    """Pixelates the image."""
    if image is None: return None
    height, width = image.shape[:2]
    temp_image = cv2.resize(image, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
    pixelated_image = cv2.resize(temp_image, (width, height), interpolation=cv2.INTER_NEAREST)
    return pixelated_image

def save_config(word):
    js_content = f'const GAME_CONFIG = {{ "word": "{word}" }};'
    with open("game_config.js", "w") as f:
        f.write(js_content)
    print(f"✅ Updated game_config.js with secret word: {word}")

def main():
    # 1. Pick a random word
    secret_word = random.choice(WORD_LIST)
    
    # 2. Search for the URL
    img_url = search_image_url(secret_word)
    
    if not img_url:
        print("Could not find an image URL. Trying another word...")
        return # In a real app, you might want to loop here to try again

    # 3. Download the actual image
    img = download_image(img_url)
    
    if img is None:
        print("Could not process image. Try running the script again.")
        return

    # 4. Create assets folder
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 5. Generate Levels
    levels = [16, 32, 64, 128] 
    
    print(f"🎨 Generating pixel levels for {secret_word}...")
    
    for i, size in enumerate(levels):
        processed_img = pixelate_image(img, size)
        cv2.imwrite(f"{OUTPUT_DIR}/level_{i+1}.jpg", processed_img)

    cv2.imwrite(f"{OUTPUT_DIR}/level_5.jpg", img)
    
    # 6. Save Config
    save_config(secret_word)
    
    print("---------------------------------------")
    print(f"GAME READY! The secret word is: {secret_word}")
    print("Refresh your web browser to play.")
    print("---------------------------------------")

if __name__ == "__main__":
    main()