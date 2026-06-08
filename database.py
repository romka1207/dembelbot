import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import config

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(config.DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                mood INTEGER,
                date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS diary_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS secret_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                photo_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None):
        self.cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        self.conn.commit()
    
    def add_mood_entry(self, user_id: int, mood: int, date: str = None):
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute('''
            INSERT INTO mood_entries (user_id, mood, date)
            VALUES (?, ?, ?)
        ''', (user_id, mood, date))
        self.conn.commit()
    
    def get_mood_entries(self, user_id: int, days: int = 30) -> List[Dict]:
        self.cursor.execute('''
            SELECT date, mood FROM mood_entries
            WHERE user_id = ? AND date >= date('now', ?)
            ORDER BY date ASC
        ''', (user_id, f'-{days} days'))
        rows = self.cursor.fetchall()
        return [{'date': row[0], 'mood': row[1]} for row in rows]
    
    def add_diary_entry(self, user_id: int, text: str):
        self.cursor.execute('''
            INSERT INTO diary_entries (user_id, text)
            VALUES (?, ?)
        ''', (user_id, text))
        self.conn.commit()
    
    def get_diary_entries(self, user_id: int = None) -> List[Dict]:
        if user_id:
            self.cursor.execute('''
                SELECT id, text, created_at FROM diary_entries
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
        else:
            self.cursor.execute('''
                SELECT id, user_id, text, created_at FROM diary_entries
                ORDER BY created_at DESC
            ''')
        rows = self.cursor.fetchall()
        if user_id:
            return [{'id': row[0], 'text': row[1], 'created_at': row[2]} for row in rows]
        else:
            return [{'id': row[0], 'user_id': row[1], 'text': row[2], 'created_at': row[3]} for row in rows]
    
    def add_secret_message(self, user_id: int, text: str, photo_id: str = None):
        self.cursor.execute('''
            INSERT INTO secret_messages (user_id, text, photo_id)
            VALUES (?, ?, ?)
        ''', (user_id, text, photo_id))
        self.conn.commit()
    
    def get_secret_messages(self, user_id: int = None) -> List[Dict]:
        if user_id:
            self.cursor.execute('''
                SELECT id, text, photo_id, created_at FROM secret_messages
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
        else:
            self.cursor.execute('''
                SELECT id, user_id, text, photo_id, created_at FROM secret_messages
                ORDER BY created_at DESC
            ''')
        rows = self.cursor.fetchall()
        if user_id:
            return [{'id': row[0], 'text': row[1], 'photo_id': row[2], 'created_at': row[3]} for row in rows]
        else:
            return [{'id': row[0], 'user_id': row[1], 'text': row[2], 'photo_id': row[3], 'created_at': row[4]} for row in rows]
    
    def close(self):
        self.conn.close()

db = Database()
