
# data-student-engineering
# Student Data Engineering Application

A modular Python data-engineering application for student academic data. The project now supports **three independent ETL sources**:

1. SQLite operational database
2. Local REST API
3. MongoDB

Each source has its own pipeline, while Transform, Validate, and Load are shared to keep the implementation consistent.

## Architecture


## Project structure



## Requirements

Python 3.10+ and a local MongoDB server.

Install the MongoDB Python driver:

pip install -r requirements.txt

Make sure MongoDB is running on:
mongodb://localhost:27017/

## Run

From the project root:

bash
python main.py


The application will:

1. Initialize SQLite.
2. Seed the SQLite demo data.
3. Start a local REST API at `/api/students`.
4. Seed MongoDB database `university`, collection `students`.
5. Run the SQLite ETL pipeline.
6. Run the API ETL pipeline.
7. Run the MongoDB ETL pipeline.
8. Validate all transformed records.
9. Export a separate CSV for each source.
10. Run the existing advanced SQL analytics.

## Output files

data/processed/student_academic_dataset_sqlite.csv
data/processed/student_academic_dataset_api.csv
data/processed/student_academic_dataset_mongodb.csv
data/analytics/student_analytics.csv
## Pipeline details

### 1. SQLite Pipeline


SQLite
  ↓ Extract
SQL JOIN
  ↓ Transform
Percentage + Grade
  ↓ Validate
Data Quality Rules
  ↓ Load
CSV

### 2. API Pipeline

The local API returns nested student documents:



The pipeline first normalizes these documents into flat ETL rows and then applies the common transformation, validation, and loading steps.

### 3. MongoDB Pipeline

MongoDB stores the same nested document structure in the `students` collection. The pipeline extracts the documents, removes MongoDB `_id` from the analytical output, normalizes the nested structure, transforms it, validates it, and loads it to CSV.

## Data quality rules

- Age: 16–80
- GPA: 0–4
- Assessment score: 0–maximum score
- Score percentage: 0–100
- Required fields must exist

## Run tests
python -m unittest discover -s tests -v

If MongoDB is not installed on Windows, Docker can start it for the project:

bash
docker compose up -d


Check the container:

docker ps

Stop it with:

docker compose down

The Python application connects to:

mongodb://localhost:27017/


## Why there are three pipelines

The three pipelines are intentionally independent:

run_sqlite_pipeline()` → extracts relational data from SQLite.
run_api_pipeline()` → extracts JSON from the REST API.
run_mongodb_pipeline()` → extracts documents from MongoDB.

All three then use the same transformation and validation rules so that the final datasets have the same schema and can be compared or combined later.
