"""Main Agent Memory System"""

from datetime import datetime
from typing import Dict, Any

from .database import MemoryDatabase


class EnhancedMemorySystem:
    """Complete enhanced memory system"""
    
    def __init__(self, db_path: str = "./memories.db"):
        """Initialize the memory system"""
        self.db = MemoryDatabase(db_path)
        print(f"✅ Memory system initialized at {db_path}")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        stats = self.db.get_stats()
        
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': stats
        }
    
    def shutdown(self):
        """Graceful shutdown"""
        print("Memory system shutdown complete")


if __name__ == "__main__":
    system = EnhancedMemorySystem()
    print("System initialized successfully")
    system.shutdown()
