import os
import random

def get_random_background():
    """
    Scans headless/assets/background-images/ and picks one background image 
    with equal probability. Returns the full file path or None if folder is empty.
    """
    # Point to headless/assets/background-images relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backgrounds_dir = os.path.abspath(os.path.join(script_dir, "..", "assets", "background-images"))

    if not os.path.exists(backgrounds_dir):
        os.makedirs(backgrounds_dir, exist_ok=True)
        print(f"Created missing directory: {backgrounds_dir}")
        return None

    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in os.listdir(backgrounds_dir) if f.lower().endswith(valid_extensions)]
    
    if not images:
        print(f"⚠️ No background images found in {backgrounds_dir}. Using solid dark theme.")
        return None

    chosen_image = random.choice(images)
    image_path = os.path.join(backgrounds_dir, chosen_image)
    print(f"🎨 Randomly selected background: {chosen_image}")
    return image_path