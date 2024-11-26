from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path

Base = declarative_base()

class APICall(Base):
    """Track API calls and usage."""
    __tablename__ = 'api_calls'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model = Column(String)
    tokens = Column(Integer)
    cost = Column(Float)
    endpoint = Column(String)
    success = Column(Integer)
    error = Column(String, nullable=True)

class AnalysisRun(Base):
    """Track analysis runs."""
    __tablename__ = 'analysis_runs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    target_path = Column(String)
    files_analyzed = Column(Integer)
    total_tokens = Column(Integer)
    total_cost = Column(Float)
    results = Column(JSON)
    status = Column(String)

class TestRun(Base):
    """Track test runs."""
    __tablename__ = 'test_runs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tests_total = Column(Integer)
    tests_passed = Column(Integer)
    tests_failed = Column(Integer)
    coverage = Column(Float)
    duration = Column(Float)
    log_path = Column(String)

def init_db():
    """Initialize database."""
    db_path = Path("crews/crew-output/monitoring.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session."""
    engine = init_db()
    Session = sessionmaker(bind=engine)
    return Session() 