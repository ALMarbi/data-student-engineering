from app.etl.extract import extract_rows
from app.etl.transform import build_processed_rows
from app.etl.validate import validate_rows
from app.etl.load import load_csv


def run_sqlite_pipeline(connection):
    raw_rows = extract_rows(connection)
    transformed_rows = build_processed_rows(raw_rows)
    validate_rows(transformed_rows)
    return load_csv(transformed_rows, "student_academic_dataset_sqlite.csv")
