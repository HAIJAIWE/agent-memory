"""SQLite-based database for memory storage"""

import sqlite3
import json
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from datetime import datetime
import threading
import hashlib

from ..models import (
    MicroMemory, SegmentMemory, MacroMemory, IndexMemory,
    MemoryType, MemoryStatus
)


class MemoryDatabase:
    """SQLite-based memory database with advanced features"""
    
    def __init__(self, db_path: str = "./memories.db", 
                 thread_safe: bool = True,
                 enable_wal: bool = True):
        self.db_path = db_path
        self.thread_safe = thread_safe
        
        if thread_safe:
            self.local = threading.local()
        else:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
        
        self._init_database(enable_wal)
    
    @contextmanager
    def get_connection(self):
        """Get thread-safe database connection"""
        if self.thread_safe:
            if not hasattr(self.local, 'conn') or self.local.conn is None:
                self.local.conn = sqlite3.connect(self.db_path)
            conn = self.local.conn
        else:
            conn = self.conn
        
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
    
    def _init_database(self, enable_wal: bool = True):
        """Initialize database schema"""
        with self.get_connection() as conn:
            if enable_wal:
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
            
            conn.execute("PRAGMA foreign_keys=ON")
            conn.execute("PRAGMA cache_size=-64000")  # 64MB
            
            self._create_tables(conn)
            conn.commit()
    
    def _create_tables(self, conn: sqlite3.Connection):
        """Create all database tables"""
        
        # Micro memory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS micro_memory (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT,
                context TEXT,
                timestamp DATETIME NOT NULL,
                parent_id TEXT,
                tags TEXT,
                metadata TEXT,
                embedding BLOB,
                embedding_hash TEXT,
                status TEXT DEFAULT 'active',
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME,
                size_bytes INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(parent_id) REFERENCES segment_memory(id)
            )
        """)
        
        # Segment memory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS segment_memory (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT,
                language TEXT,
                micro_ids TEXT,
                timestamp DATETIME NOT NULL,
                last_modified DATETIME NOT NULL,
                status TEXT DEFAULT 'active',
                parent_id TEXT,
                relations TEXT,
                metadata TEXT,
                embedding BLOB,
                priority INTEGER DEFAULT 5,
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME,
                size_bytes INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(parent_id) REFERENCES macro_memory(id)
            )
        """)
        
        # Macro memory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS macro_memory (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                segment_ids TEXT,
                structure TEXT,
                timestamp DATETIME NOT NULL,
                last_modified DATETIME NOT NULL,
                status TEXT DEFAULT 'active',
                relations TEXT,
                metadata TEXT,
                priority INTEGER DEFAULT 5,
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Index memory table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS index_memory (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                references TEXT,
                summary TEXT,
                tags TEXT,
                keywords TEXT,
                priority INTEGER DEFAULT 5,
                relations TEXT,
                last_accessed DATETIME,
                access_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Relations table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id TEXT PRIMARY KEY,
                from_id TEXT NOT NULL,
                to_id TEXT NOT NULL,
                relation_type TEXT,
                strength REAL DEFAULT 1.0,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(from_id, to_id, relation_type)
            )
        """)
        
        # Create indexes
        indexes = [
            ("idx_micro_type", "micro_memory", "type"),
            ("idx_segment_type", "segment_memory", "type"),
            ("idx_relations_from", "relations", "from_id"),
        ]
        
        for idx_name, table, column in indexes:
            conn.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})")
        
        # Full-text search tables
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS micro_search USING fts5(
                id UNINDEXED,
                content,
                context,
                tags
            )
        """)
    
    def store_micro(self, memory: MicroMemory, embedding: Optional[bytes] = None) -> str:
        """Store micro-level memory"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            content_hash = hashlib.md5(memory.content.encode()).hexdigest()
            size = len(memory.content.encode('utf-8'))
            
            cursor.execute("""
                INSERT OR REPLACE INTO micro_memory 
                (id, type, content, content_hash, context, timestamp, parent_id, 
                 tags, metadata, embedding, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.type.value,
                memory.content,
                content_hash,
                memory.context,
                memory.timestamp,
                memory.parent_id,
                json.dumps(memory.tags or []),
                json.dumps(memory.metadata or {}),
                embedding,
                size
            ))
            
            conn.commit()
            return memory.id
    
    def get_micro(self, memory_id: str) -> Optional[MicroMemory]:
        """Get micro-level memory by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM micro_memory WHERE id = ?", (memory_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            columns = [d[0] for d in cursor.description]
            data = dict(zip(columns, row))
            
            return self._dict_to_micro_memory(data)
    
    def store_segment(self, memory: SegmentMemory, embedding: Optional[bytes] = None) -> str:
        """Store segment-level memory"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            content_hash = hashlib.md5(memory.content.encode()).hexdigest()
            size = len(memory.content.encode('utf-8'))
            
            cursor.execute("""
                INSERT OR REPLACE INTO segment_memory
                (id, type, title, content, content_hash, language, micro_ids,
                 timestamp, last_modified, status, parent_id, relations, 
                 metadata, embedding, priority, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.type.value,
                memory.title,
                memory.content,
                content_hash,
                memory.language,
                json.dumps(memory.micro_ids),
                memory.timestamp,
                memory.last_modified,
                memory.status.value,
                memory.parent_id,
                json.dumps(memory.relations or {}),
                json.dumps(memory.metadata or {}),
                embedding,
                memory.priority,
                size
            ))
            
            conn.commit()
            return memory.id
    
    def get_segment(self, memory_id: str) -> Optional[SegmentMemory]:
        """Get segment-level memory by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM segment_memory WHERE id = ?", (memory_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            columns = [d[0] for d in cursor.description]
            data = dict(zip(columns, row))
            return self._dict_to_segment_memory(data)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            for table in ['micro_memory', 'segment_memory', 'macro_memory', 'index_memory']:
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE status = 'active'")
                stats[f'{table}_count'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(size_bytes) FROM micro_memory WHERE status = 'active'")
            micro_size = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(size_bytes) FROM segment_memory WHERE status = 'active'")
            segment_size = cursor.fetchone()[0] or 0
            
            stats['total_size_bytes'] = micro_size + segment_size
            stats['total_size_mb'] = (micro_size + segment_size) / (1024 * 1024)
            
            return stats
    
    def _dict_to_micro_memory(self, data: Dict) -> MicroMemory:
        """Convert dict to MicroMemory object"""
        return MicroMemory(
            id=data['id'],
            type=MemoryType(data['type']),
            content=data['content'],
            context=data.get('context'),
            timestamp=datetime.fromisoformat(data['timestamp']),
            metadata=json.loads(data.get('metadata', '{}')),
            parent_id=data.get('parent_id'),
            tags=json.loads(data.get('tags', '[]'))
        )
    
    def _dict_to_segment_memory(self, data: Dict) -> SegmentMemory:
        """Convert dict to SegmentMemory object"""
        return SegmentMemory(
            id=data['id'],
            type=MemoryType(data['type']),
            title=data['title'],
            content=data['content'],
            language=data.get('language'),
            micro_ids=json.loads(data.get('micro_ids', '[]')),
            timestamp=datetime.fromisoformat(data['timestamp']),
            last_modified=datetime.fromisoformat(data['last_modified']),
            status=MemoryStatus(data.get('status', 'active')),
            metadata=json.loads(data.get('metadata', '{}')),
            parent_id=data.get('parent_id'),
            relations=json.loads(data.get('relations', '{}'))
        )
