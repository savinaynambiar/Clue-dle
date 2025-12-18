import cv2
import os

# CONFIGURATION
IMAGE_NAME = "scooter.jpg"  # Put your image file name here
OUTPUT_DIR = "assets"       # Where the game images will be saved

def pixelate_image(image, pixel_size):
    """
    Pixelates an image by downsizing and then upsizing.
    pixel_size: The width/height of the small intermediate image.
    Lower number = More blocky/Harder to guess.
    """
    height, width = image.shape[:2]
    
    # 1. Downscale to small size (removes detail)
    temp_image = cv2.resize(image, (pixel_size, pixel_size), interpolation=cv2.INTER_LINEAR)
    
    # 2. Upscale back to original size (makes it blocky)
    # INTER_NEAREST is crucial for that sharp "pixel art" look
    pixelated_image = cv2.resize(temp_image, (width, height), interpolation=cv2.INTER_NEAREST)
    
    return pixelated_image

def main():
    # 1. Load the secret image
    if not os.path.exists(IMAGE_NAME):
        print(f"Error: Could not find {IMAGE_NAME}. Please add an image to this folder.")
        return

    img = cv2.imread(IMAGE_NAME)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 2. Generate 5 Levels of Difficulty
    # Level 1 (Hardest): 16x16 grid
    # Level 5 (Easiest): Original Image
    
    levels = [16, 32, 64, 128] # Resolution sizes for levels 1-4
    
    print(f"Processing {IMAGE_NAME}...")

    # Generate Levels 1 to 4
    for i, size in enumerate(levels):
        processed_img = pixelate_image(img, size)
        filename = f"{OUTPUT_DIR}/level_{i+1}.jpg"
        cv2.imwrite(filename, processed_img)
        print(f"Saved: {filename}")

    # Level 5 is the original clear image
    cv2.imwrite(f"{OUTPUT_DIR}/level_5.jpg", img)
    print(f"Saved: {OUTPUT_DIR}/level_5.jpg")
    
    print("Done! Check your 'assets' folder.")

if __name__ == "__main__":
    main()