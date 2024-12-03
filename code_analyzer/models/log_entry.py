"""Log entry model."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from datetime import datetime
from code_analyzer.models.base import Base

class LogEntry(Base):
    """Log entry model."""
    __tablename__ = 'log_entries'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    message = Column(String)
    crew_name = Column(String)
    extra_data = Column(JSON)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.level,
            'message': self.message,
            'crew_name': self.crew_name,
            'metadata': self.extra_data or {}
        }
