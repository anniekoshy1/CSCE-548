# create_db.py
# Usage: python create_db.py
import sqlite3
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
DB_FILE = ROOT / "homework.db"
SCHEMA = ROOT / "schema.sql"
SEED = ROOT / "seed.sql"

def run_sql_file(conn, path):
    print(f"Running {path.name} ...")
    sql = path.read_text(encoding="utf-8")
    conn.executescript(sql)

def main():
    if not SCHEMA.exists():
        print("schema.sql not found in the current folder. Make sure you're in the repo folder.")
        sys.exit(1)

    # create DB and apply schema
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        run_sql_file(conn, SCHEMA)
        # run seed if available
        if SEED.exists():
            run_sql_file(conn, SEED)
        conn.commit()
    finally:
        conn.close()

    # verify tables and counts
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [r["name"] for r in cur.fetchall()]
    print("\nCreated tables:", tables)

    # if assignments table exists, show count
    if "assignments" in tables:
        cur.execute("SELECT COUNT(*) AS c FROM assignments;")
        print("assignments count:", cur.fetchone()["c"])
    conn.close()
    print("\nDone. You can now run `python app.py`.")
    
if __name__ == "__main__":
    main()
