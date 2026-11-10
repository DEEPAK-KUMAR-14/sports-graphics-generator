import os
import sys
import json

# Add scripts directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
from background_selector import get_random_background
from image_renderer import render_football_graphic

def process_match_files():
    base_dir = os.path.dirname(__file__)
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    formats_dir = os.path.join(base_dir, "formats")

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Load output formatting configuration
    try:
        with open(os.path.join(formats_dir, "output_format.json"), "r") as f:
            output_config = json.load(f)
    except Exception as e:
        print(f"❌ Error loading output_format.json: {e}")
        return

    # Scan input folder for JSON queue files
    input_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]
    if not input_files:
        print(f"⚠️ No JSON files found in {input_dir}. Add match data files to process.")
        return

    for file_name in input_files:
        input_file_path = os.path.join(input_dir, file_name)
        print(f"\n📂 Processing file: {file_name}")

        try:
            with open(input_file_path, "r", encoding="utf-8") as f:
                match_data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading {file_name}: {e}")
            continue

        # Dynamic Sport Detection (Supports football, formula1, etc. dynamically)
        sport_type = match_data.get("sport", "").lower()
        if not sport_type or sport_type not in match_data:
            print(f"❌ Skipped {file_name}: Missing or invalid 'sport' field.")
            continue

        sport_payload = match_data[sport_type]
        sport_conf = output_config.get(sport_type, {"format": "WebP", "quality": 90})
        
        # Determine file extension based on format configuration
        output_ext = ".webp" if sport_conf.get("format", "WebP").lower() == "webp" else ".jpg"
        base_name = os.path.splitext(file_name)[0]
        output_filename = f"{base_name}{output_ext}"
        output_file_path = os.path.join(output_dir, output_filename)

        # Get random background using our module
        random_bg_path = get_random_background()

        # Render graphic based on sport type
        if sport_type == "football":
            render_football_graphic(sport_payload, random_bg_path, output_file_path, sport_conf)
            print(f"✅ Success! Football graphic generated: output/{output_filename}")
            
        elif sport_type == "formula1":
            # Future expansion slot for Formula 1 rendering module!
            print(f"ℹ️ Formula 1 rendering schema detected for {file_name}. (Module can be hooked up here next!)")

if __name__ == "__main__":
    process_match_files()