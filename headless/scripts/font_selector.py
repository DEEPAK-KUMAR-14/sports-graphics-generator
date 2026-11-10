# import os
# import random
# import requests
# from PIL import ImageFont

# def get_styled_font(category, size):
#     """
#     Picks a random font from headless/assets/fonts/normal/ or headless/assets/fonts/quirky/.
#     Prints the selected font for debugging and falls back safely if folders are empty.
#     """
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#     font_category_dir = os.path.join(base_dir, "assets", "fonts", category)
#     os.makedirs(font_category_dir, exist_ok=True)
    
#     font_files = [f for f in os.listdir(font_category_dir) if f.lower().endswith(('.ttf', '.otf'))]
    
#     if font_files:
#         chosen_font_name = random.choice(font_files)
#         chosen_font_path = os.path.join(font_category_dir, chosen_font_name)
#         try:
#             font = ImageFont.truetype(chosen_font_path, size)
#             print(f"🔤 Loaded [{category}] font: {chosen_font_name} (size {size})")
#             return font
#         except Exception as e:
#             print(f"⚠️ Warning: Could not load font {chosen_font_path}: {e}")

#     # Fallback if category folder is empty
#     print(f"⚠️ Warning: No fonts found in '{category}/' folder! Using Oswald fallback.")
#     fallback_path = os.path.join(base_dir, "assets", "fonts", "Oswald-Bold.ttf")
    
#     if not os.path.exists(fallback_path):
#         try:
#             font_url = "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
#             with open(fallback_path, "wb") as f:
#                 f.write(requests.get(font_url, timeout=10).content)
#         except Exception:
#             pass

#     try:
#         return ImageFont.truetype(fallback_path, size)
#     except IOError:
#         print("❌ Error: Truetype failed completely. Using default tiny font.")
#         return ImageFont.load_default()