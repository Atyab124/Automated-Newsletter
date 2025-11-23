"""
SQLite database management for Newsletter Generator
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import DATABASE_PATH


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Topics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_name TEXT NOT NULL UNIQUE,
                frequency TEXT NOT NULL,
                last_run DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Writing samples table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS writing_samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,
                text TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            )
        """)
        
        # Fact sheets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_sheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                markdown TEXT NOT NULL,
                json_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            )
        """)
        
        # Newsletters table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS newsletters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                markdown TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_topic(self, topic_name: str, frequency: str) -> int:
        """Add a new topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO topics (topic_name, frequency)
                VALUES (?, ?)
            """, (topic_name, frequency))
            conn.commit()
            topic_id = cursor.lastrowid
            return topic_id
        except sqlite3.IntegrityError:
            raise ValueError(f"Topic '{topic_name}' already exists")
        finally:
            conn.close()
    
    def get_topic(self, topic_id: int) -> Optional[Dict]:
        """Get topic by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_topics(self) -> List[Dict]:
        """Get all topics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topics ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def update_topic_last_run(self, topic_id: int, last_run: datetime):
        """Update topic's last run time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE topics
            SET last_run = ?
            WHERE id = ?
        """, (last_run.isoformat(), topic_id))
        conn.commit()
        conn.close()
    
    def add_writing_sample(self, topic_id: int, text: str) -> int:
        """Add writing sample"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO writing_samples (topic_id, text)
            VALUES (?, ?)
        """, (topic_id, text))
        conn.commit()
        sample_id = cursor.lastrowid
        conn.close()
        return sample_id
    
    def get_writing_samples(self, topic_id: int) -> List[Dict]:
        """Get writing samples for a topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM writing_samples
            WHERE topic_id = ?
            ORDER BY created_at DESC
        """, (topic_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def save_fact_sheet(self, topic_id: int, markdown: str, json_data: Dict) -> int:
        """Save fact sheet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fact_sheets (topic_id, markdown, json_data)
            VALUES (?, ?, ?)
        """, (topic_id, markdown, json.dumps(json_data)))
        conn.commit()
        sheet_id = cursor.lastrowid
        conn.close()
        return sheet_id
    
    def get_latest_fact_sheet(self, topic_id: int) -> Optional[Dict]:
        """Get latest fact sheet for a topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM fact_sheets
            WHERE topic_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (topic_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_fact_sheets(self, topic_id: int) -> List[Dict]:
        """Get all fact sheets for a topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM fact_sheets
            WHERE topic_id = ?
            ORDER BY created_at DESC
        """, (topic_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def save_newsletter(self, topic_id: int, markdown: str) -> int:
        """Save newsletter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO newsletters (topic_id, markdown)
            VALUES (?, ?)
        """, (topic_id, markdown))
        conn.commit()
        newsletter_id = cursor.lastrowid
        conn.close()
        return newsletter_id
    
    def get_latest_newsletter(self, topic_id: int) -> Optional[Dict]:
        """Get latest newsletter for a topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM newsletters
            WHERE topic_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (topic_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_newsletters(self, topic_id: int) -> List[Dict]:
        """Get all newsletters for a topic"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM newsletters
            WHERE topic_id = ?
            ORDER BY created_at DESC
        """, (topic_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

