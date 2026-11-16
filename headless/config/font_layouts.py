# headless/config/font_layouts.py

FONT_LAYOUTS = {
    # --- FALLBACK DEFAULT PROFILE ---
    "default": {
        "score_size": 80,
        "score_y": 215,
        "score_color": (52, 211, 153, 255),       # Vibrant Mint Green
        "team_size": 38,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),      # Crisp White
    },

    # --- ASIMOVIAN ---
    "asimovian": {
        "score_size": 100,
        "score_y": 220,
        "score_color": (52, 211, 153, 255),
        "team_size": 40,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- AUDIOWIDE ---
    "audiowide": {
        "score_size": 70,
        "score_y": 225,
        "score_color": (56, 189, 248, 255),      # Electric Sky Blue
        "team_size": 34,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- BANGERS (PRIMARY FONT - OPTIMIZED FOR MOBILE LEGIBILITY) ---
    # Multi-comment safety block preserving your exact primary styling setup:
    # "score_size": 140, "score_y": 195, "score_color": (250, 204, 21, 255) [Trophy Gold]
    # "team_size": 52, "team_y": 315, "team_color": (255, 255, 255, 255) [Crisp White]
    "bangers": {
        "score_size": 160,
        "score_y": 195,
        "score_color": (250, 204, 21, 255),      # Trophy Gold
        "team_size": 66,                         # Bold & legible mobile font size
        "team_y": 360,                           # Positioned directly below the 165px logo (ends at 295)
        "team_color": (255, 255, 255, 255),
    },

    # --- BBHBOGLE ---
    "bbhbogle": {
        "score_size": 80,
        "score_y": 215,
        "score_color": (52, 211, 153, 255),
        "team_size": 38,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- BLACK OPS ONE ---
    "blackopsone": {
        "score_size": 75,
        "score_y": 220,
        "score_color": (244, 63, 94, 255),      # Bold Red Accent
        "team_size": 35,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- BUNGEE ---
    "bungee": {
        "score_size": 65,
        "score_y": 230,
        "score_color": (250, 204, 21, 255),
        "team_size": 30,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- CINZEL DECORATIVE ---
    "cinzeldecorative": {
        "score_size": 75,
        "score_y": 220,
        "score_color": (250, 204, 21, 255),
        "team_size": 36,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- MERIENDA ---
    "merienda": {
        "score_size": 70,
        "score_y": 222,
        "score_color": (52, 211, 153, 255),
        "team_size": 34,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- MOMO TRUST DISPLAY ---
    "momotrustdisplay": {
        "score_size": 75,
        "score_y": 220,
        "score_color": (52, 211, 153, 255),
        "team_size": 36,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- OUTFIT ---
    "outfit": {
        "score_size": 80,
        "score_y": 215,
        "score_color": (52, 211, 153, 255),
        "team_size": 38,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- PERMANENT MARKER ---
    "permanentmarker": {
        "score_size": 75,
        "score_y": 218,
        "score_color": (250, 204, 21, 255),
        "team_size": 36,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    },

    # --- SCIENCE GOTHIC ---
    "sciencegothic": {
        "score_size": 78,
        "score_y": 216,
        "score_color": (52, 211, 153, 255),
        "team_size": 37,
        "team_y": 315,
        "team_color": (255, 255, 255, 255),
    }
}

def get_font_layout(font_filename):
    """
    Normalizes the filename (strips spaces, dashes, and lowercases) 
    to match against custom tuning blocks safely.
    """
    clean_key = font_filename.lower().replace("-", "").replace("_", "").replace(" ", "").replace(".ttf", "").replace(".otf", "")
    
    for key, layout in FONT_LAYOUTS.items():
        if key in clean_key:
            return layout
            
    return FONT_LAYOUTS["default"]