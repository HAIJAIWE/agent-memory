"""Memory data models for the hierarchical memory system"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any


class MemoryLevel(Enum):
    """Memory hierarchy levels"""
    MICRO = "micro"        # Hundreds of characters
    SEGMENT = "segment"    # 1-5K characters
    MACRO = "macro"        # 10K+ characters
    INDEX = "index"        # Tens of characters


class MemoryType(Enum):
    """Memory content types"""
    CODE = "code"
    STORY = "story"
    TASK = "task"
    DECISION = "decision"
    MODIFICATION = "modification"
    RELATION = "relation"


class MemoryStatus(Enum):
    """Memory lifecycle status"""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


@dataclass
class MicroMemory:
    """Micro-level memory: single operation, decision point"""
    id: str
    type: MemoryType
    content: str              # Hundreds of characters
    context: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class SegmentMemory:
    """Segment-level memory: single file, chapter, or feature"""
    id: str
    type: MemoryType
    title: str
    content: str              # 1-5K characters
    language: Optional[str] = None
    micro_ids: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    status: MemoryStatus = MemoryStatus.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    relations: Dict[str, List[str]] = field(default_factory=dict)
    priority: int = 5


@dataclass
class MacroMemory:
    """Macro-level memory: complete project, large system"""
    id: str
    type: MemoryType
    title: str
    description: str
    segment_ids: List[str] = field(default_factory=list)
    structure: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    status: MemoryStatus = MemoryStatus.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)
    relations: Dict[str, List[str]] = field(default_factory=dict)
    priority: int = 5


@dataclass
class IndexMemory:
    """Index memory: fast navigation, quick lookup"""
    id: str
    title: str
    type: MemoryType
    references: List[str]     # Pointers to micro/segment/macro
    summary: str              # Tens to hundreds of characters
    tags: List[str] = field(default_factory=list)
    priority: int = 5
    keywords: List[str] = field(default_factory=list)
    relations: Dict[str, List[str]] = field(default_factory=dict)
    last_accessed: Optional[datetime] = None
    access_count: int = 0
