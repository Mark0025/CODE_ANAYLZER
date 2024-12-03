"""Track development history and progress."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from code_analyzer.models.base import Base

class DevelopmentEvent(Base):
    """Track development events and milestones."""
    __tablename__ = 'development_events'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)  # 'commit', 'conversation', 'milestone', etc.
    title = Column(String)
    description = Column(Text)
    event_data = Column(JSON)  # Renamed from metadata
    
    # Relationships
    files_changed = relationship("FileChange", back_populates="event")
    conversations = relationship("CursorConversation", back_populates="event")
    documentation = relationship("DocumentationChange", back_populates="event")

class FileChange(Base):
    """Track file changes."""
    __tablename__ = 'file_changes'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    file_path = Column(String)
    change_type = Column(String)  # 'add', 'modify', 'delete'
    content_before = Column(Text, nullable=True)
    content_after = Column(Text, nullable=True)
    change_data = Column(JSON)  # Renamed from metadata
    
    event = relationship("DevelopmentEvent", back_populates="files_changed")

class CursorConversation(Base):
    """Track Cursor AI conversations."""
    __tablename__ = 'cursor_conversations'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    conversation_id = Column(String)
    prompt = Column(Text)
    response = Column(Text)
    conversation_data = Column(JSON)  # Renamed from metadata
    
    event = relationship("DevelopmentEvent", back_populates="conversations")

class DocumentationChange(Base):
    """Track documentation evolution."""
    __tablename__ = 'documentation_changes'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    doc_path = Column(String)
    content = Column(Text)
    doc_data = Column(JSON)  # Renamed from metadata
    
    event = relationship("DevelopmentEvent", back_populates="documentation") 