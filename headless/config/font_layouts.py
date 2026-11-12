# headless/config/font_layouts.py

FONT_LAYOUTS = {
    # --- FALLBACK DEFAULT PROFILE ---
    "default": {
        "score_size": 80,
        "score_y": 215,
        "score_color": (52, 211, 153, 255),       # Vibrant Mint Green
        "team_size": 38,
        "team_y": 275,
        "team_color": (255, 255, 255, 255),      # Crisp White
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),   # Slate Light Gray
    },

    # --- ASIMOVIAN ---
    "asimovian": {
        "score_size": 100,
        "score_y": 220,
        "score_color": (52, 211, 153, 255),
        "team_size": 40,
        "team_y": 278,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 30,
        "scorers_y": 380,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- AUDIOWIDE ---
    "audiowide": {
        "score_size": 70,
        "score_y": 225,
        "score_color": (56, 189, 248, 255),      # Electric Sky Blue
        "team_size": 34,
        "team_y": 280,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- BANGERS ---
    "bangers": {
        "score_size": 110,
        "score_y": 205,
        "score_color": (250, 204, 21, 255),      # Trophy Gold
        "team_size": 60,
        "team_y": 270,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 30,
        "scorers_y": 340,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- BBHBOGLE ---
    "bbhbogle": {
        "score_size": 80,
        "score_y": 215,
        "score_color": (52, 211, 153, 255),
        "team_size": 38,
        "team_y": 275,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- BLACK OPS ONE ---
    "blackopsone": {
        "score_size": 75,
        "score_y": 220,
        "score_color": (244, 63, 94, 255),      # Bold Red Accent
        "team_size": 35,
        "team_y": 278,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- BUNGEE ---
    "bungee": {
        "score_size": 65,
        "score_y": 230,
        "score_color": (250, 204, 21, 255),
        "team_size": 30,
        "team_y": 285,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- CINZEL DECORATIVE ---
    "cinzeldecorative": {
        "score_size": 75,
        "score_y": 220,
        "score_color": (250, 204, 21, 255),
        "team_size": 36,
        "team_y": 278,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- MERIENDA ---
    "merienda": {
        "score_size": 70,
        "score_y": 222,
        "score_color": (52, 211, 153, 255),
        "team_size": 34,
        "team_y": 278,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- MOMO TRUST DISPLAY ---
    "momotrustdisplay": {
        "score_size": 75,
        "score_y": 220,
        "score_color": (52, 211, 153, 255),
        "team_size": 36,
        "team_y": 275,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },


    # --- OUTFIT ---
    "outfit": {
        "score_size": 80,
        "score_y": 215,
        "score_color": (52, 211, 153, 255),
        "team_size": 38,
        "team_y": 275,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- PERMANENT MARKER ---
    "permanentmarker": {
        "score_size": 75,
        "score_y": 218,
        "score_color": (250, 204, 21, 255),
        "team_size": 36,
        "team_y": 276,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
    },

    # --- SCIENCE GOTHIC ---
    "sciencegothic": {
        "score_size": 78,
        "score_y": 216,
        "score_color": (52, 211, 153, 255),
        "team_size": 37,
        "team_y": 275,
        "team_color": (255, 255, 255, 255),
        "scorers_size": 20,
        "scorers_y": 335,
        "scorers_color": (203, 213, 225, 255),
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



# "yourfontname": {
#         "score_size": 80,
#         "score_y": 215,
#         "score_color": (52, 211, 153, 255),
#         "team_size": 38,
#         "team_y": 275,
#         "team_color": (255, 255, 255, 255),
#         "scorers_size": 20,
#         "scorers_y": 335,
#         "scorers_color": (203, 213, 225, 255),
#     },