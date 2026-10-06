from app.etl.normalize import flatten_student_documents
from app.etl.raw import save_raw_json
from app.etl.transform import build_processed_rows
from app.etl.validate import validate_rows
from app.etl.load import load_csv
from app.sources.mongodb import extract_mongo


def run_mongodb_pipeline(
    uri: str = "mongodb://localhost:27017/",
    database: str = "university",
    collection: str = "students",
):
    documents = extract_mongo(uri, database, collection)
    save_raw_json(documents, "mongodb_students.json")
    raw_rows = flatten_student_documents(documents)
    transformed_rows = build_processed_rows(raw_rows)
    validate_rows(transformed_rows)
    return load_csv(transformed_rows, "student_academic_dataset_mongodb.csv")
