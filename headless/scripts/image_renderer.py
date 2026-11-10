import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw

# Import our modular font selector from scripts/
from font_selector import get_font_path, get_styled_font

# Try importing cairosvg (Primary SVG renderer)
try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False

# Try importing svglib (Backup SVG renderer)
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    HAS_SVGLIB = True
except ImportError:
    HAS_SVGLIB = False

def load_team_logo(logos_dir, logo_name, size=(100, 100)):
    """
    Tries to load a team logo supporting extension-less JSON names (e.g. 'barca').
    Uses cairosvg as primary renderer and svglib as fallback backup for SVGs.
    """
    if not logo_name:
        return None

    extensions = ["", ".svg", ".png", ".jpg", ".jpeg"]
    logo_path = None
    
    for ext in extensions:
        potential_path = os.path.join(logos_dir, logo_name + ext if not logo_name.endswith(ext) else logo_name)
        if os.path.exists(potential_path):
            logo_path = potential_path
            break

    if not logo_path or not os.path.exists(logo_path):
        print(f"⚠️ Logo file not found for: '{logo_name}' in {logos_dir}")
        return None

    ext = os.path.splitext(logo_path)[1].lower()

    if ext == ".svg":
        png_data = None
        if HAS_CAIROSVG:
            try:
                png_data = cairosvg.svg2png(url=logo_path, output_width=size[0], output_height=size[1])
            except Exception as e:
                print(f"CairoSVG failed for {logo_path}: {e}")

        if not png_data and HAS_SVGLIB:
            try:
                drawing = svg2rlg(logo_path)
                img_io = BytesIO()
                renderPM.drawToFile(drawing, img_io, fmt="PNG")
                img_io.seek(0)
                png_data = img_io.read()
            except Exception as e:
                print(f"Svglib failed for {logo_path}: {e}")

        if png_data:
            try:
                return Image.open(BytesIO(png_data)).resize(size).convert("RGBA")
            except Exception as e:
                print(f"Error converting SVG bytecode: {e}")
                return None
        else:
            return None
    else:
        try:
            return Image.open(logo_path).resize(size).convert("RGBA")
        except Exception as e:
            print(f"Warning: Could not open raster logo: {e}")
            return None

def render_football_graphic(sport_payload, bg_path, output_file_path, output_config):
    width, height = 1200, 630
    canvas = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    
    # 1. Apply background image and background dimness overlay
    if bg_path and os.path.exists(bg_path):
        try:
            bg = Image.open(bg_path).resize((width, height)).convert("RGBA")
            
            # --- BACKGROUND DIMNESS CONTROL ---
            # OPTION A (Current / Default): Dark blue tint with medium-high dimness (180 alpha) for best text readability
            # overlay = Image.new("RGBA", (width, height), (10, 15, 30, 180))
            
            # OPTION B (Lighter Dimness): Lower the alpha value (e.g., 100 instead of 180) for a brighter background
            overlay = Image.new("RGBA", (width, height), (10, 15, 30, 100))
            
            # OPTION C (No Dimness / Original Brightness): To remove dimness completely, comment out or delete 
            # the 'overlay =' line above, and comment out the 'canvas = Image.alpha_composite(...)' line below.
            # ----------------------------------

            canvas.paste(bg, (0, 0))
            canvas = Image.alpha_composite(canvas, overlay) # Remove or comment this line if using Option C (No Dimness)
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")

    draw = ImageDraw.Draw(canvas)
    
    # 2. Pick ONE Quirky font path and ONE Normal font path for consistent styling across the entire image
    quirky_path = get_font_path("quirky")
    normal_path = get_font_path("normal")

    # Load sizes using the exact same font files
    font_score = get_styled_font(quirky_path, 80)
    font_teams = get_styled_font(quirky_path, 38)
    font_small = get_styled_font(normal_path, 22)
    font_scorers = get_styled_font(normal_path, 22)

    league = sport_payload.get("leagueName", "FOOTBALL MATCH")
    team_a = sport_payload["teamA"]
    team_b = sport_payload["teamB"]

    # 3. Draw Header Badge (Normal Font)
    draw.rectangle([60, 45, 260, 90], fill=(225, 29, 72, 255))
    draw.text((75, 52), league.upper(), fill=(255, 255, 255, 255), font=font_small)

    # 4. Draw Score Box Center (Quirky Font)
    score_text = f"{team_a['score']}  -  {team_b['score']}"
    score_bbox = draw.textbbox((0, 0), score_text, font=font_score)
    score_w = score_bbox[2] - score_bbox[0]
    score_x = (width - score_w) / 2
    score_y = 220
    
    draw.rounded_rectangle([score_x - 40, score_y - 15, score_x + score_w + 40, score_y + 90], radius=20, fill=(30, 41, 59, 230))
    draw.text((score_x, score_y), score_text, fill=(52, 211, 153, 255), font=font_score)

    logos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "team-logos"))

    # 5. Team A (Left side) - Quirky Font for Name
    logo_a = load_team_logo(logos_dir, team_a.get("logoName", ""), size=(90, 90))
    if logo_a:
        canvas.paste(logo_a, (175, 170), logo_a)
        
    team_a_name = team_a["name"]
    name_a_bbox = draw.textbbox((0, 0), team_a_name, font=font_teams)
    name_a_w = name_a_bbox[2] - name_a_bbox[0]
    draw.text((220 - (name_a_w / 2), 275), team_a_name, fill=(255, 255, 255, 255), font=font_teams)
    
    # Scorers Team A (Normal Font)
    scorers_a = team_a.get("scorers", [])
    if scorers_a:
        scorers_a_text = "\n".join([f"- {s}" for s in scorers_a])
        draw.text((140, 330), scorers_a_text, fill=(203, 213, 225, 255), font=font_scorers)

    # 6. Team B (Right side) - Quirky Font for Name
    logo_b = load_team_logo(logos_dir, team_b.get("logoName", ""), size=(90, 90))
    if logo_b:
        canvas.paste(logo_b, (935, 170), logo_b)
        
    team_b_name = team_b["name"]
    name_b_bbox = draw.textbbox((0, 0), team_b_name, font=font_teams)
    name_b_w = name_b_bbox[2] - name_b_bbox[0]
    draw.text((980 - (name_b_w / 2), 275), team_b_name, fill=(255, 255, 255, 255), font=font_teams)

    # Scorers Team B (Normal Font)
    scorers_b = team_b.get("scorers", [])
    if scorers_b:
        scorers_b_text = "\n".join([f"- {s}" for s in scorers_b])
        draw.text((900, 330), scorers_b_text, fill=(203, 213, 225, 255), font=font_scorers)

    # 7. Footer Branding (Normal Font)
    draw.text((60, 560), "Automated Headless Engine • Powered by Python & PIL", fill=(148, 163, 184, 255), font=font_small)

    # 8. Save Output File
    format_type = output_config.get("format", "WebP").lower()
    quality = output_config.get("quality", 90)
    
    final_image = canvas.convert("RGB")
    if format_type == "webp":
        final_image.save(output_file_path, "WEBP", quality=quality)
    else:
        final_image.save(output_file_path, "JPEG", quality=quality)