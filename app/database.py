# app/database.py

import duckdb
import os

def get_db_connection():
    db_path = os.getenv("DUCKDB_PATH", "data/bom.duckdb")
    conn = duckdb.connect(database=db_path, read_only=False)

    conn.execute("CREATE SEQUENCE IF NOT EXISTS parts_id_seq START WITH 1 INCREMENT BY 1")

    # BOM table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS parts (
                 id INTEGER PRIMARY KEY DEFAULT nextval('parts_id_seq'),
                 name VARCHAR NOT NULL,
                 quantity INTEGER NOT NULL,
                 unit_pcs VARCHAR DEFAULT 'pcs',
                 material VARCHAR,
                 mass_value_eur FLOAT,
                 mass_unit_kg VARCHAR,
                 project_extra_eur FLOAT,
                 description TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                 )
                 """)
    
    return conn