from __future__ import annotations

import sqlite3
import sys
from flask import Flask, Response, jsonify, render_template, g

from init_db import DATABASE_PATH, initialize_database

# Ensure that the SQLite database exists and has the expected schema so that
# API requests do not fail with "no such table" errors when the application is
# started without running the separate initialization script beforehand.
if "--init-db" not in sys.argv:
    initialize_database()

app = Flask(__name__)


@app.route("/favicon.ico")
def favicon() -> Response:
    """Serve the application favicon to avoid unnecessary 404 errors."""
    return app.send_static_file("favicon.ico")


def get_db() -> sqlite3.Connection:
    """Open a new database connection for the current request."""
    if "db" not in g:
        connection = sqlite3.connect(DATABASE_PATH)
        connection.row_factory = sqlite3.Row

        try:
            connection.execute("SELECT 1 FROM category LIMIT 1")
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            # If the schema is missing or the SQLite file is corrupted,
            # recreate it and reopen the connection so subsequent queries work.
            connection.close()
            DATABASE_PATH.unlink(missing_ok=True)
            initialize_database()
            connection = sqlite3.connect(DATABASE_PATH)
            connection.row_factory = sqlite3.Row

        g.db = connection
    return g.db


def init_db() -> None:
    """Reset the database file and load the default sample data."""
    DATABASE_PATH.unlink(missing_ok=True)
    initialize_database()


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
    if "--init-db" in sys.argv:
        init_db()
        print("✅ Datenbank erfolgreich initialisiert.")
    else:
        app.run(debug=True)
