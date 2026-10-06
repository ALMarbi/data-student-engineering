from app.etl.normalize import flatten_student_documents
from app.etl.raw import save_raw_json
from app.etl.transform import build_processed_rows
from app.etl.validate import validate_rows
from app.etl.load import load_csv
from app.sources.mock_api import extract_api


def run_api_pipeline(url: str = "http://127.0.0.1:8765/api/students"):
    documents = extract_api(url)
    save_raw_json(documents, "api_students.json")
    raw_rows = flatten_student_documents(documents)
    transformed_rows = build_processed_rows(raw_rows)
    validate_rows(transformed_rows)
    return load_csv(transformed_rows, "student_academic_dataset_api.csv")
