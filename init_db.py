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

SEED_DATA = {
    "Rückenmassage": [30, 45],
    "Aromatherapie": [45, 60],
    "Sportmassage": [30, 60, 90],
}


def initialize_database() -> None:
    DATABASE_PATH.touch(exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.executescript(SCHEMA)

        for category_name, durations in SEED_DATA.items():
            cursor.execute(
                "INSERT OR IGNORE INTO category(name) VALUES (?)",
                (category_name,),
            )
            cursor.execute(
                "SELECT id FROM category WHERE name = ?",
                (category_name,),
            )
            category_id = cursor.fetchone()[0]

            for duration in durations:
                treatment_name = f"{category_name} — {duration} Minuten"
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO treatment(name, duration_minutes, category_id)
                    VALUES (?, ?, ?)
                    """,
                    (treatment_name, duration, category_id),
                )

        connection.commit()


if __name__ == "__main__":
    initialize_database()
    print("Die Datenbank wurde initialisiert und mit Beispieldaten befüllt.")
