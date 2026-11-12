import os
import random
import requests
from PIL import ImageFont

# ==========================================
# 🛠️ DEBUG OVERRIDE CONTROL
# ==========================================
# Set this to a string filename if you want to FORCE a specific font (e.g., "Bangers-Regular.ttf").
# Leave it as None when you want the engine to pick randomly.
FORCED_DEBUG_FONT = "Bangers-Regular.ttf"
# FORCED_DEBUG_FONT = none
# FORCED_DEBUG_FONT = "Bangers-Regular.ttf"  <-- Uncomment to test a specific font
# ==========================================

def get_font_selection(category):
    """
    Picks a font file from headless/assets/fonts/normal/ or quirky/ 
    and returns both the absolute file path and the filename (so layout configs can match it).
    Supports a forced override for easy design testing.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    fonts_root = os.path.join(base_dir, "assets", "fonts")
    
    category_dir = os.path.join(fonts_root, category)
    if not os.path.exists(category_dir):
        category_dir = os.path.join(fonts_root, category.lower())
        
    os.makedirs(category_dir, exist_ok=True)
    
    font_files = [f for f in os.listdir(category_dir) if f.lower().endswith(('.ttf', '.otf'))]
    
    # 1. Check if we forced a specific font for debugging (and it matches the quirky category)
    global FORCED_DEBUG_FONT
    if FORCED_DEBUG_FONT and category.lower() == "quirky":
        forced_path = os.path.join(category_dir, FORCED_DEBUG_FONT)
        if os.path.exists(forced_path):
            print(f"🔒 [DEBUG MODE] Forced [{category}] font: {FORCED_DEBUG_FONT}")
            return forced_path, FORCED_DEBUG_FONT
        else:
            print(f"⚠️ Warning: Forced debug font '{FORCED_DEBUG_FONT}' not found in {category}/. Falling back to random.")

    # 2. Standard random selection
    if font_files:
        chosen_font_name = random.choice(font_files)
        chosen_font_path = os.path.join(category_dir, chosen_font_name)
        print(f"🔤 Selected [{category}] font: {chosen_font_name}")
        return chosen_font_path, chosen_font_name

    # 3. Fallback if category folder is empty
    print(f"⚠️ Warning: No valid .ttf/.otf fonts found in '{category}/'! Using Oswald fallback.")
    fallback_path = os.path.join(fonts_root, "Oswald-Bold.ttf")
    
    if not os.path.exists(fallback_path):
        try:
            font_url = "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
            with open(fallback_path, "wb") as f:
                f.write(requests.get(font_url, timeout=10).content)
        except Exception:
            pass

    return fallback_path, "Oswald-Bold.ttf"

def get_styled_font(font_path, size):
    """
    Loads a specific font file path at the requested size.
    """
    try:
        return ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"⚠️ Warning: Could not load font at {font_path}: {e}")
        return ImageFont.load_default()