from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, g

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "massage.db"

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    """Open a new database connection for the current request."""
    if "db" not in g:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


@app.teardown_appcontext
def close_db(exception: Exception | None) -> None:
    """Close the database connection at the end of the request lifecycle."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index() -> str:
    """Render the main interface."""
    return render_template("index.html")


@app.route("/api/categories")
def categories() -> str:
    """Return available massage categories."""
    db = get_db()
    rows = db.execute(
        "SELECT id, name FROM category ORDER BY name COLLATE NOCASE"
    ).fetchall()
    data = [dict(row) for row in rows]
    return jsonify(data)


@app.route("/api/treatments/<int:category_id>")
def treatments(category_id: int) -> str:
    """Return treatments for the selected category."""
    db = get_db()
    rows = db.execute(
        """
        SELECT id, name, duration_minutes
        FROM treatment
        WHERE category_id = ?
        ORDER BY duration_minutes
        """,
        (category_id,),
    ).fetchall()
    data = [dict(row) for row in rows]
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
