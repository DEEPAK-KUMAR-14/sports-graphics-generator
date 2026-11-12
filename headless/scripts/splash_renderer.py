# headless/scripts/splash_renderer.py
import os
import random
from PIL import Image

def apply_paint_splash(canvas, score_x, score_y, score_w, splash_color=(52, 211, 153, 200)):
    """
    Pastes a grunge/paint splash texture right behind the score container 
    between the background and the text layer.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    splash_dir = os.path.join(base_dir, "assets", "splashes")
    os.makedirs(splash_dir, exist_ok=True)
    
    splash_files = [f for f in os.listdir(splash_dir) if f.lower().endswith(('.png', '.webp'))]
    
    if not splash_files:
        print(f"⚠️ Warning: No splash images found in '{splash_dir}/'. Skipping paint splash effect.")
        return canvas

    # Pick a random splash asset
    chosen_splash = random.choice(splash_files)
    splash_path = os.path.join(splash_dir, chosen_splash)
    
    try:
        splash_img = Image.open(splash_path).convert("RGBA")
        
        # Scale the splash relative to the score box width (make it wider and punchy)
        target_w = int(score_w * 1.8)
        aspect_ratio = splash_img.height / splash_img.width
        target_h = int(target_w * aspect_ratio)
        
        splash_img = splash_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Optional: Tint the splash to match a specific color (like neon green or gold) if desired
        # if splash_color:
        #     # Create a colored overlay using the splash alpha channel as a mask
        #     color_layer = Image.new("RGBA", splash_img.size, splash_color)
        #     # Use the splash's own transparency channel to mask the tint
        #     splash_img = Image.composite(color_layer, splash_img, splash_img)

        # Calculate positioning to center the splash perfectly behind the score box
        paste_x = int(score_x - (target_w - score_w) / 2)
        paste_y = int(score_y - 25) # Shift slightly up to frame the score box nicely
        
        # Create a transparent container to paste the splash onto, then alpha composite
        splash_canvas = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        splash_canvas.paste(splash_img, (paste_x, paste_y), splash_img)
        
        canvas = Image.alpha_composite(canvas, splash_canvas)
        print(f"🎨 Applied paint splash: {chosen_splash}")
        return canvas

    except Exception as e:
        print(f"⚠️ Warning: Could not render paint splash: {e}")
        return canvas