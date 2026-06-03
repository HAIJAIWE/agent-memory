"""Tests for database module"""

import pytest
from src.database import MemoryDatabase
from src.models import MicroMemory, SegmentMemory, MemoryType


class TestMemoryDatabase:
    """Test MemoryDatabase functionality"""
    
    @pytest.fixture
    def db(self):
        """Create a test database"""
        return MemoryDatabase(":memory:")
    
    def test_store_micro_memory(self, db):
        """Test storing micro memory"""
        micro = MicroMemory(
            id="test_1",
            type=MemoryType.CODE,
            content="test content",
            tags=["test"]
        )
        
        result = db.store_micro(micro)
        assert result == "test_1"
    
    def test_get_micro_memory(self, db):
        """Test retrieving micro memory"""
        micro = MicroMemory(
            id="test_2",
            type=MemoryType.CODE,
            content="test content"
        )
        
        db.store_micro(micro)
        retrieved = db.get_micro("test_2")
        
        assert retrieved is not None
        assert retrieved.id == "test_2"
    
    def test_store_segment_memory(self, db):
        """Test storing segment memory"""
        segment = SegmentMemory(
            id="seg_1",
            type=MemoryType.CODE,
            title="Test",
            content="content"
        )
        
        result = db.store_segment(segment)
        assert result == "seg_1"
