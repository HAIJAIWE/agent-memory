"""Basic usage examples for the Agent Memory System"""

from src.memory_system import EnhancedMemorySystem
from src.models import MicroMemory, SegmentMemory, MemoryType, MemoryStatus


def example_initialization():
    """Example: Initialize the memory system"""
    print("="*60)
    print("Example: Basic Initialization")
    print("="*60)
    
    memory = EnhancedMemorySystem()
    health = memory.get_system_health()
    print(f"Status: {health.get('status')}")


def example_store_memory():
    """Example: Store memories"""
    print("\n" + "="*60)
    print("Example: Store Memory")
    print("="*60)
    
    memory = EnhancedMemorySystem()
    
    # Create and store a micro memory
    micro = MicroMemory(
        id="micro_001",
        type=MemoryType.CODE,
        content="def hello_world():\n    print('Hello, World!')",
        tags=["python", "example"]
    )
    
    memory.db.store_micro(micro)
    print("✅ Stored micro memory")
    
    # Create and store a segment memory
    segment = SegmentMemory(
        id="seg_001",
        type=MemoryType.CODE,
        title="Binary Search",
        content="def binary_search(arr, target): ...",
        language="python"
    )
    
    memory.db.store_segment(segment)
    print("✅ Stored segment memory")


if __name__ == "__main__":
    example_initialization()
    example_store_memory()
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
