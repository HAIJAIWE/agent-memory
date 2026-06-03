# Agent Memory System Architecture

## Overview

The Agent Memory System is a hierarchical, distributed memory system designed for AI agents.

## Core Concepts

### Memory Hierarchy

The system uses a 4-level hierarchy:

- **Micro**: Single operations (100-500 chars)
- **Segment**: Files/chapters (1-5K chars)
- **Macro**: Projects/systems (10K+ chars)
- **Index**: Navigation/routing (10-100 chars)

## System Architecture

### Storage Layer
- SQLite database with FTS5 full-text search
- Vector indexing for semantic search
- Four-level memory hierarchy

### Retrieval Layer
- Semantic search (vector-based)
- Keyword search (FTS5-based)
- Hybrid search (combined)
- Relation-based search (graph traversal)

### Enhancement Layer
- Deduplication
- Summarization
- Version control
- Monitoring

## Data Model

```python
@dataclass
class MicroMemory:
    id: str                    # Unique identifier
    type: MemoryType           # CODE, STORY, TASK, etc.
    content: str               # Main content
    context: Optional[str]     # Context information
    timestamp: datetime        # When created
    metadata: Dict[str, Any]   # Flexible metadata
    parent_id: Optional[str]   # Link to parent segment
    tags: List[str]            # Classification tags
```

## Performance Characteristics

- **Storage**: Unlimited (distributed via archival)
- **Retrieval**: O(1) for cached, O(log n) for indexed
- **Concurrency**: Thread-safe database with WAL mode
- **Memory**: Configurable based on available RAM

## Scalability

- Supports millions of memories
- Automatic archival of old memories
- Deduplication to reduce storage
- Hierarchical storage with lazy loading
