"""
storage.py
Módulo para manejar el almacenamiento en SQLite.
Provee funciones CRUD para artículos.
"""
import sqlite3
import datetime

class Storage:
    def __init__(self, db_path="budget.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def ensure_tables(self):
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """)
            conn.commit()

    def create(self, name, category, quantity, unit_price, description=None):
        now = datetime.datetime.utcnow().isoformat()
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO items (name, category, quantity, unit_price, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, category, quantity, unit_price, description, now, now))
            conn.commit()
            return c.lastrowid

    def list_all(self):
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM items ORDER BY id")
            return c.fetchall()

    def search(self, q):
        q_like = f"%{q}%"
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM items WHERE name LIKE ? OR category LIKE ? ORDER BY id", (q_like, q_like))
            return c.fetchall()

    def get_by_id(self, id_):
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM items WHERE id = ?", (id_,))
            return c.fetchone()

    def update(self, id_, name, category, quantity, unit_price, description):
        now = datetime.datetime.utcnow().isoformat()
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("""
            UPDATE items SET name=?, category=?, quantity=?, unit_price=?, description=?, updated_at=?
            WHERE id=?
            """, (name, category, quantity, unit_price, description, now, id_))
            conn.commit()

    def delete(self, id_):
        with self._conn() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM items WHERE id = ?", (id_,))
            conn.commit()
