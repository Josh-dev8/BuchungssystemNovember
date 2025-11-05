from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "massage.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS treatment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    FOREIGN KEY(category_id) REFERENCES category(id)
);
"""

SAMPLE_DATA = {
    "Rückenmassage": [
        ("Kurz (30 Minuten)", 30),
        ("Lang (60 Minuten)", 60),
    ],
    "Aromatherapie": [
        ("Sanft (45 Minuten)", 45),
    ],
    "Sportmassage": [
        ("Intensiv (90 Minuten)", 90),
    ],
}


def _populate_database(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.executescript(SCHEMA)

    for category_name, treatments in SAMPLE_DATA.items():
        cursor.execute(
            "INSERT OR IGNORE INTO category(name) VALUES (?)",
            (category_name,),
        )
        cursor.execute(
            "SELECT id FROM category WHERE name = ?",
            (category_name,),
        )
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError(
                f"Kategorie '{category_name}' konnte nicht angelegt werden."
            )
        category_id = row[0]

        for treatment_name, duration in treatments:
            cursor.execute(
                """
                INSERT OR IGNORE INTO treatment(name, duration_minutes, category_id)
                VALUES (?, ?, ?)
                """,
                (treatment_name, duration, category_id),
            )

    connection.commit()


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            _populate_database(connection)
    except sqlite3.DatabaseError:
        # Falls die Datei beschädigt ist, neu anlegen und nochmals befüllen.
        DATABASE_PATH.unlink(missing_ok=True)
        with sqlite3.connect(DATABASE_PATH) as connection:
            _populate_database(connection)


if __name__ == "__main__":
    initialize_database()
    print("Die Datenbank wurde initialisiert und mit Beispieldaten befüllt.")
