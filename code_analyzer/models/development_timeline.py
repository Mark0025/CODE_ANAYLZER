"""Development timeline tracking."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from code_analyzer.models.base import Base

class DevelopmentEvent(Base):
    """Track development events and milestones."""
    __tablename__ = 'development_events'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)  # 'commit', 'crew_operation', 'test_run', 'shell_command'
    title = Column(String)
    description = Column(Text)
    event_data = Column(JSON)  # Store additional context
    
    # Relationships
    files_changed = relationship("FileChange", back_populates="event")
    shell_commands = relationship("ShellCommand", back_populates="event")
    crew_operations = relationship("CrewOperation", back_populates="event")
    test_results = relationship("TestResult", back_populates="event")

class FileChange(Base):
    """Track file changes."""
    __tablename__ = 'file_changes'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    file_path = Column(String)
    change_type = Column(String)  # 'add', 'modify', 'delete'
    content_before = Column(Text, nullable=True)
    content_after = Column(Text, nullable=True)
    change_data = Column(JSON)  # Store diff, stats, etc.
    
    event = relationship("DevelopmentEvent", back_populates="files_changed")

class ShellCommand(Base):
    """Track shell command executions."""
    __tablename__ = 'shell_commands'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    command = Column(String)
    status = Column(Integer)  # Exit code
    output = Column(Text)
    error = Column(Text, nullable=True)
    command_data = Column(JSON)  # Store environment, timing, etc.
    
    event = relationship("DevelopmentEvent", back_populates="shell_commands")

class CrewOperation(Base):
    """Track crew operations."""
    __tablename__ = 'crew_operations'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    crew_name = Column(String)
    operation = Column(String)
    status = Column(String)
    result = Column(JSON)
    operation_data = Column(JSON)  # Store performance metrics, etc.
    
    event = relationship("DevelopmentEvent", back_populates="crew_operations")

class TestResult(Base):
    """Track test executions."""
    __tablename__ = 'test_results'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('development_events.id'))
    test_name = Column(String)
    status = Column(String)  # 'pass', 'fail', 'error'
    duration = Column(Float)
    error_message = Column(Text, nullable=True)
    test_data = Column(JSON)  # Store coverage, etc.
    
    event = relationship("DevelopmentEvent", back_populates="test_results")