from sqlalchemy import create_engine, inspect, text
from app.config import settings
from pymongo import MongoClient

pg = create_engine(settings.database_url)
mongo = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
mongo.admin.command("ping")

db = mongo["qsr_db"]
tables = inspect(pg).get_table_names()

for table in tables:
    with pg.connect() as conn:
        rows = conn.execute(text(f'SELECT * FROM "{table}"')).mappings().all()
        documents = [dict(row) for row in rows]

    collection = db[table]
    collection.delete_many({})
    if documents:
        collection.insert_many(documents)

    print(f"{table}: {len(documents)} documents copied")

print("\nPostgreSQL -> MongoDB copy completed.")
mongo.close()
