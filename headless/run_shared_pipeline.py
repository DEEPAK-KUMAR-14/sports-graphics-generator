import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv


def _resolve_shared_dir(project_root: Path) -> Path:
    raw = os.getenv("SHARED_FOLDER_DIR", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (project_root.parent / "shared_folder").resolve()


def main() -> None:
    headless_dir = Path(__file__).resolve().parent
    project_root = headless_dir.parent

    # Load .env from project root first, then headless/ if present
    load_dotenv(project_root / ".env")
    load_dotenv(headless_dir / ".env", override=False)

    shared_dir = _resolve_shared_dir(project_root)
    shared_input = shared_dir / "input"
    shared_output = shared_dir / "output"
    shared_processed = shared_dir / "processed"

    local_input = project_root / "input"
    local_output = project_root / "output"
    generator_script = headless_dir / "generator.py"

    print(f"[shared] Using shared folder: {shared_dir}")
    print(f"[env] Using Python: {sys.executable}")

    for folder in (shared_input, shared_output, shared_processed, local_input, local_output):
        folder.mkdir(parents=True, exist_ok=True)

    json_files = sorted(shared_input.glob("*.json"))
    if not json_files:
        print(f"[shared] No new JSON files in {shared_input}")
        return

    for src_json in json_files:
        dst_json = local_input / src_json.name
        shutil.copy2(src_json, dst_json)
        print(f"[in] Copied {src_json.name} -> {dst_json}")

    subprocess.run([sys.executable, str(generator_script)], cwd=str(headless_dir), check=True)

    for src_json in json_files:
        stem = src_json.stem
        generated = [
            p
            for p in local_output.iterdir()
            if p.is_file()
            and p.stem == stem
            and p.suffix.lower() in {".webp", ".jpg", ".jpeg", ".png"}
        ]
        for img_path in generated:
            dst_img = shared_output / img_path.name
            shutil.copy2(img_path, dst_img)
            print(f"[out] Copied {img_path.name} -> {dst_img}")

        shutil.move(str(src_json), str(shared_processed / src_json.name))

    print("[done] Shared pipeline cycle complete.")


if __name__ == "__main__":
    main()