import os
import random
import requests
from PIL import ImageFont

def get_font_path(category):
    """
    Picks a single random font file path from headless/assets/fonts/normal/ or quirky/ 
    so it can be reused consistently across multiple text elements on the same graphic.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fonts_root = os.path.join(base_dir, "assets", "fonts")
    
    category_dir = os.path.join(fonts_root, category)
    if not os.path.exists(category_dir):
        category_dir = os.path.join(fonts_root, category.lower())
        
    os.makedirs(category_dir, exist_ok=True)
    
    font_files = [f for f in os.listdir(category_dir) if f.lower().endswith(('.ttf', '.otf'))]
    
    if font_files:
        chosen_font_name = random.choice(font_files)
        chosen_font_path = os.path.join(category_dir, chosen_font_name)
        print(f"🔤 Selected [{category}] font: {chosen_font_name}")
        return chosen_font_path

    # Fallback if category folder is empty
    print(f"⚠️ Warning: No valid .ttf/.otf fonts found in '{category}/'! Using Oswald fallback.")
    fallback_path = os.path.join(fonts_root, "Oswald-Bold.ttf")
    
    if not os.path.exists(fallback_path):
        try:
            font_url = "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
            with open(fallback_path, "wb") as f:
                f.write(requests.get(font_url, timeout=10).content)
        except Exception:
            pass

    return fallback_path

def get_styled_font(font_path, size):
    """
    Loads a specific font file path at the requested size.
    """
    try:
        return ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"⚠️ Warning: Could not load font at {font_path}: {e}")
        return ImageFont.load_default()