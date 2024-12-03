"""Models for crew outputs and analysis results."""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from code_analyzer.models.base import Base

class CrewOutput(Base):
    """Base model for crew outputs."""
    __tablename__ = 'crew_outputs'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    crew_name = Column(String)
    output = Column(JSON)

class ErrorHandlingResult(Base):
    """Model for error handling results."""
    __tablename__ = 'error_handling_results'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_type = Column(String)
    details = Column(JSON)

class CodeAnalysisResult(Base):
    """Model for code analysis results."""
    __tablename__ = 'code_analysis_results'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    analysis_data = Column(JSON)