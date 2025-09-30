import sqlite3
from pathlib import Path

DB_PATH = Path("todo.db") # Const declaration with the path of database


def create_connection():
    """Creates and return a connction with databases."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return connection

def init_db():
    """Cria a tabela tasks se não existir."""
    connection = create_connection()
    with connection:  # The 'with' managemnt the close automaticaly
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                done BOOLEAN NOT NULL CHECK (done IN (0, 1)) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    # Don't close manual — o 'with' close this