import csv
from app.utils.paths import PROCESSED_DIR


def load_csv(rows, filename="student_academic_dataset.csv"):
    if not rows:
        raise ValueError("No processed rows to export.")

    output_file = PROCESSED_DIR / filename
    fieldnames = list(rows[0].keys())

    with output_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_file
