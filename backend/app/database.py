from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os

Base = declarative_base()

class CVSession(Base):
    """Database model for CV analysis sessions."""
    __tablename__ = "cv_sessions"
    
    id = Column(String, primary_key=True)
    cv_text = Column(Text, nullable=False)
    cv_file_type = Column(String, nullable=False)
    cv_file_path = Column(String)
    
    # Job analysis data
    job_title = Column(String)
    job_description = Column(Text)
    
    # Analysis results
    original_score = Column(Integer)
    new_score = Column(Integer)
    missing_skills = Column(JSON)
    strengths = Column(JSON)
    experience_gaps = Column(JSON)
    recommendations = Column(JSON)
    summary = Column(Text)
    
    # Enhancement data
    additional_info = Column(Text)
    improvement_suggestions = Column(JSON)
    enhanced_cv_path = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    """Database model for users (optional for future expansion)."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cv_analyzer.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables if they don't exist."""
    Base.metadata.create_all(bind=engine, checkfirst=True)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
