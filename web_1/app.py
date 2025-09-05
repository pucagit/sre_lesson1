from flask import Flask, render_template, redirect, url_for # type: ignore
import sqlite3
import aiosqlite # type: ignore

DB_PATH = "my_database.db"

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL") # Enable WAL mode for better concurrency
        cur.execute("""
            CREATE TABLE IF NOT EXISTS access (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                count INTEGER NOT NULL
            )
        """)
        # Ensure there is exactly one row (id=1)
        cur.execute("""
            INSERT INTO access (id, count)
            SELECT 1, 0
            WHERE NOT EXISTS (SELECT 1 FROM access WHERE id = 1)
        """)
        conn.commit()
    finally:
        conn.close()

init_db()

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))

@app.get("/")
async def hello_world():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN IMMEDIATE")
        cursor = await db.execute(
            "UPDATE access SET count = count + 1 WHERE id = 1 RETURNING count"
        )
        row = await cursor.fetchone()
        count = row[0] if row else 0
        await db.commit()

    return render_template('index.html', count=count)
