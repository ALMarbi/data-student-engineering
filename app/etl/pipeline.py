"""Backward-compatible ETL entry point plus source-specific pipelines."""

from app.etl.pipelines.sqlite_pipeline import run_sqlite_pipeline
from app.etl.pipelines.api_pipeline import run_api_pipeline
from app.etl.pipelines.mongodb_pipeline import run_mongodb_pipeline


def run_pipeline(connection):
    """Keep the original API: the default pipeline is SQLite."""
    return run_sqlite_pipeline(connection)


def run_all_source_pipelines(
    connection,
    api_url="http://127.0.0.1:8765/api/students",
    mongo_uri="mongodb://localhost:27017/",
    mongo_database="university",
    mongo_collection="students",
):
    results = {"sqlite": run_sqlite_pipeline(connection)}
    results["api"] = run_api_pipeline(api_url)
    results["mongodb"] = run_mongodb_pipeline(
        mongo_uri, mongo_database, mongo_collection
    )
    return results
