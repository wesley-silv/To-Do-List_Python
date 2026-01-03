import sqlite3
from pathlib import Path # Destinated for work with paths of files
from typing import Union


# Implementation of tests
DB_PATH: Union[str, Path] = "app.db" # Const declaration with the path of database


def set_db_path(path: Union[str, Path]):
    """Permite mudar o caminho do banco (útil para testes)."""
    global DB_PATH
    DB_PATH = path

def create_connection():
    """Creates and return a connection with databases."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # This allow us access the columns by name
    # print("Object connection created:", type(connection))
    return connection # Return the connection object

def init_db():
    """Creates a tasks table if not existr."""
    connection = create_connection()
    with connection:  # The 'with' managemnt the close automaticaly
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                done BOOLEAN NOT NULL CHECK (done IN (0, 1)) DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now', 'utc'))
            );
        """)