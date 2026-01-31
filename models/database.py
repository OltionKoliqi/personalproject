import sqlite3
from config import DATABASE_NAME

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(
                DATABASE_NAME,
                check_same_thread=False,
                timeout=30
            )
            cls._instance.conn.execute("PRAGMA journal_mode=WAL;")
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_tables()
        return cls._instance

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            math INTEGER,
            science INTEGER,
            english INTEGER,
            total INTEGER,
            average REAL,
            grade TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
        """)

        self.conn.commit()
