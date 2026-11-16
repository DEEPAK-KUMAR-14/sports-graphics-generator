import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from font_selector import get_font_selection, get_styled_font
from text_formatter import wrap_team_name
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.font_layouts import get_font_layout

try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False

try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    HAS_SVGLIB = True
except ImportError:
    HAS_SVGLIB = False

def load_team_logo(logos_dir, logo_name, size=(100, 100)):
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
        return None
    ext = os.path.splitext(logo_path)[1].lower()
    if ext == ".svg":
        png_data = None
        if HAS_CAIROSVG:
            try:
                png_data = cairosvg.svg2png(url=logo_path, output_width=size[0], output_height=size[1])
            except Exception:
                pass
        if not png_data and HAS_SVGLIB:
            try:
                drawing = svg2rlg(logo_path)
                img_io = BytesIO()
                renderPM.drawToFile(drawing, img_io, fmt="PNG")
                img_io.seek(0)
                png_data = img_io.read()
            except Exception:
                pass
        if png_data:
            try:
                return Image.open(BytesIO(png_data)).resize(size).convert("RGBA")
            except Exception:
                return None
    else:
        try:
            return Image.open(logo_path).resize(size).convert("RGBA")
        except Exception:
            return None

def resize_and_crop_background(img, target_width, target_height):
    img_width, img_height = img.size
    img_ratio = img_width / img_height
    target_ratio = target_width / target_height
    if img_ratio > target_ratio:
        new_height = target_height
        new_width = int(new_height * img_ratio)
    else:
        new_width = target_width
        new_height = int(new_width / img_ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    return img.crop((left, top, left + target_width, top + target_height))

def render_fixture_graphic(sport_payload, bg_path, output_file_path, output_config):
    width, height = 1200, 630
    canvas = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    MARGIN = 60
    
    if bg_path and os.path.exists(bg_path):
        try:
            bg = Image.open(bg_path).convert("RGBA")
            bg = resize_and_crop_background(bg, width, height)
            overlay = Image.new("RGBA", (width, height), (10, 15, 30, 120))
            canvas.paste(bg, (0, 0))
            canvas = Image.alpha_composite(canvas, overlay)
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")

    draw = ImageDraw.Draw(canvas)
    
    quirky_path, quirky_filename = get_font_selection("quirky")
    normal_path, _ = get_font_selection("normal")
    layout = get_font_layout(quirky_filename)

    font_score = get_styled_font(quirky_path, layout["score_size"])
    font_teams = get_styled_font(quirky_path, layout["team_size"])
    font_small = get_styled_font(normal_path, 22)

    league = sport_payload.get("leagueName", "FOOTBALL MATCH")
    team_a = sport_payload["teamA"]
    team_b = sport_payload["teamB"]

    # 1. Top Left League Badge
    badge_x, badge_y = MARGIN, MARGIN
    league_text = league.upper()
    league_bbox = draw.textbbox((0, 0), league_text, font=font_small)
    league_w = league_bbox[2] - league_bbox[0]
    draw.rectangle([badge_x, badge_y, badge_x + league_w + 40, badge_y + 45], fill=(60, 221, 133, 255))
    draw.text((badge_x + 20, badge_y + 9), league_text, fill=(255, 255, 255, 255), font=font_small)

    # 2. Top Right Branding Badge
    brand_text = "THETOPTEN.IN"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=font_small)
    brand_w = brand_bbox[2] - brand_bbox[0]
    brand_right = width - MARGIN
    draw.rectangle([brand_right - brand_w - 40, badge_y, brand_right, badge_y + 45], fill=(0, 28, 214, 255))
    draw.text((brand_right - brand_w - 20, badge_y + 9), brand_text, fill=(255, 255, 255, 255), font=font_small)

    # 3. Center "VS" Element
    score_text = "VS"
    score_bbox = draw.textbbox((0, 0), score_text, font=font_score)
    score_w = score_bbox[2] - score_bbox[0]
    score_x = (width - score_w) / 2
    score_y = layout["score_y"]
    draw.text((score_x, score_y), score_text, fill=layout["score_color"], font=font_score)

    logos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "team-logos"))

    # 4. Team A (Left)
    logo_a_size = 150
    logo_a_x = MARGIN + 40
    logo_a = load_team_logo(logos_dir, team_a.get("logoName", ""), size=(logo_a_size, logo_a_size))
    if logo_a:
        canvas.paste(logo_a, (logo_a_x, 145), logo_a)
        
    team_a_name_wrapped = wrap_team_name(team_a["name"], max_chars_per_line=15)
    name_a_bbox = draw.multiline_textbbox((0, 0), team_a_name_wrapped, font=font_teams, align="center")
    name_a_w = name_a_bbox[2] - name_a_bbox[0]
    team_a_center_x = logo_a_x + (logo_a_size / 2)
    draw.multiline_text(
        (max(MARGIN, team_a_center_x - (name_a_w / 2)), layout["team_y"]), 
        team_a_name_wrapped, fill=layout["team_color"], font=font_teams, align="center"
    )

    # 5. Team B (Right)
    logo_b_x = width - MARGIN - logo_a_size - 40
    logo_b = load_team_logo(logos_dir, team_b.get("logoName", ""), size=(logo_a_size, logo_a_size))
    if logo_b:
        canvas.paste(logo_b, (logo_b_x, 145), logo_b)
        
    team_b_name_wrapped = wrap_team_name(team_b["name"], max_chars_per_line=15)
    name_b_bbox = draw.multiline_textbbox((0, 0), team_b_name_wrapped, font=font_teams, align="center")
    name_b_w = name_b_bbox[2] - name_b_bbox[0]
    team_b_center_x = logo_b_x + (logo_a_size / 2)
    draw.multiline_text(
        (team_b_center_x - (name_b_w / 2), layout["team_y"]), 
        team_b_name_wrapped, fill=layout["team_color"], font=font_teams, align="center"
    )

    # 6. Fixture Hook Text (Cleanly centered horizontally, adjustable size & vertical position)
    hook_text = sport_payload.get("fixtureHookText", "MATCHDAY PREVIEW • H2H & LINEUP").upper()
    
    # 🎛️ Adjust font size here (e.g., change 24 to 20 for smaller, or 30 for larger)
    font_hook = get_styled_font(normal_path, 56)
    
    hook_bbox = draw.textbbox((0, 0), hook_text, font=font_hook)
    hook_w = hook_bbox[2] - hook_bbox[0]
    hook_x = (width - hook_w) / 2
    
    # 🎛️ Adjust vertical position here (Higher number = further down towards the bottom margin)
    hook_y = 480
    
    draw.text((hook_x, hook_y), hook_text, fill=(250, 204, 21, 255), font=font_hook) # Trophy Gold

    # 7. Save WebP (Under 300KB)
    format_type = output_config.get("format", "WebP").lower()
    quality = output_config.get("quality", 85)
    final_image = canvas.convert("RGB")
    if format_type == "webp":
        final_image.save(output_file_path, "WEBP", quality=quality, method=6)
    else:
        final_image.save(output_file_path, "JPEG", quality=quality)