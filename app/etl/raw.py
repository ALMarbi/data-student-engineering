import json
from app.utils.paths import RAW_DIR


def save_raw_json(data, filename):
    output_file = RAW_DIR / filename
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, default=str)
    return output_file
