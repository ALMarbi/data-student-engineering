"""MongoDB source and demo seeding helpers."""

from __future__ import annotations


def get_client(uri: str = "mongodb://localhost:27017/", timeout_ms: int = 5000):
    try:
        from pymongo import MongoClient
    except ImportError as exc:
        raise RuntimeError(
            "MongoDB source requires pymongo. Install it with: pip install pymongo"
        ) from exc

    return MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)


def seed_mongo_demo(
    uri: str = "mongodb://localhost:27017/",
    database: str = "university",
    collection: str = "students",
) -> int:
    from app.sources.mock_api import build_demo_payload

    with get_client(uri) as client:
        db = client[database]
        coll = db[collection]
        coll.delete_many({})
        docs = build_demo_payload()
        if docs:
            coll.insert_many(docs)
        return len(docs)


def extract_mongo(
    uri: str = "mongodb://localhost:27017/",
    database: str = "university",
    collection: str = "students",
    timeout_ms: int = 5000,
) -> list[dict]:
    with get_client(uri, timeout_ms) as client:
        client.admin.command("ping")
        return list(client[database][collection].find({}, {"_id": 0}))
