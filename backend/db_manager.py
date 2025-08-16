#!/usr/bin/env python3
"""
Database management script for CV Analyzer.
Provides utilities for database operations.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.database import create_tables, SessionLocal, engine
from app.crud import CVSessionCRUD, UserCRUD
from sqlalchemy import text
import argparse

def create_db():
    """Create database tables."""
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")

def list_sessions():
    """List all CV sessions with detailed information."""
    db = SessionLocal()
    try:
        sessions = CVSessionCRUD.get_all_sessions(db)
        print(f"\nFound {len(sessions)} CV analysis jobs:")
        print("=" * 100)
        print(f"{'ID':<15} {'Job Title':<20} {'Score':<8} {'Improved':<8} {'Type':<6} {'Created':<12} {'Status':<10}")
        print("=" * 100)
        
        for session in sessions:
            job_title = (session.job_title or "N/A")[:19]
            original_score = f"{session.original_score or 0}/100"
            improvement = f"+{session.new_score - session.original_score}" if session.new_score and session.original_score else "N/A"
            file_type = session.cv_file_type
            created = session.created_at.strftime("%Y-%m-%d")
            
            # Determine status
            status = "Complete" if session.enhanced_cv_path else "Analyzed" if session.original_score else "Uploaded"
            
            print(f"{session.id:<15} {job_title:<20} {original_score:<8} {improvement:<8} {file_type:<6} {created:<12} {status:<10}")
            
        print("=" * 100)
        print(f"Summary: {len(sessions)} total jobs")
        
    finally:
        db.close()

def clean_db():
    """Clean up old sessions and orphaned files."""
    db = SessionLocal()
    try:
        sessions = CVSessionCRUD.get_all_sessions(db)
        cleaned_files = 0
        
        for session in sessions:
            # Check and clean up CV files
            if session.cv_file_path and os.path.exists(session.cv_file_path):
                # Keep files for now, just report
                pass
            elif session.cv_file_path:
                print(f"Orphaned CV file reference: {session.cv_file_path}")
                
            # Check enhanced CV files
            if session.enhanced_cv_path and os.path.exists(session.enhanced_cv_path):
                # Keep files for now, just report
                pass
            elif session.enhanced_cv_path:
                print(f"Orphaned enhanced CV file reference: {session.enhanced_cv_path}")
                cleaned_files += 1
        
        print(f"Database cleanup complete. Found {cleaned_files} orphaned file references.")
        
    finally:
        db.close()

def reset_db():
    """Reset database (WARNING: This will delete all data!)."""
    confirm = input("WARNING: This will delete ALL data! Type 'yes' to continue: ")
    if confirm.lower() == 'yes':
        print("Dropping all tables...")
        from app.database import Base
        Base.metadata.drop_all(bind=engine)
        print("Recreating tables...")
        create_tables()
        print("Database reset complete!")
    else:
        print("Operation cancelled.")

def show_stats():
    """Show database statistics."""
    db = SessionLocal()
    try:
        # Get session count
        result = db.execute(text("SELECT COUNT(*) FROM cv_sessions")).fetchone()
        session_count = result[0] if result else 0
        
        # Get sessions with analysis
        result = db.execute(text("SELECT COUNT(*) FROM cv_sessions WHERE original_score IS NOT NULL")).fetchone()
        analyzed_count = result[0] if result else 0
        
        # Get sessions with enhancement
        result = db.execute(text("SELECT COUNT(*) FROM cv_sessions WHERE enhanced_cv_path IS NOT NULL")).fetchone()
        enhanced_count = result[0] if result else 0
        
        # Get average scores
        result = db.execute(text("SELECT AVG(original_score) FROM cv_sessions WHERE original_score IS NOT NULL")).fetchone()
        avg_original_score = round(result[0], 2) if result and result[0] else 0
        
        result = db.execute(text("SELECT AVG(new_score) FROM cv_sessions WHERE new_score IS NOT NULL")).fetchone()
        avg_new_score = round(result[0], 2) if result and result[0] else 0
        
        print("\n📊 Database Statistics")
        print("=" * 50)
        print(f"Total CV Sessions: {session_count}")
        print(f"Analyzed CVs: {analyzed_count}")
        print(f"Enhanced CVs: {enhanced_count}")
        print(f"Average Original Score: {avg_original_score}")
        print(f"Average Enhanced Score: {avg_new_score}")
        print(f"Average Improvement: {round(avg_new_score - avg_original_score, 2)}")
        
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CV Analyzer Database Management")
    parser.add_argument("command", choices=["create", "list", "clean", "reset", "stats"], 
                       help="Database operation to perform")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_db()
    elif args.command == "list":
        list_sessions()
    elif args.command == "clean":
        clean_db()
    elif args.command == "reset":
        reset_db()
    elif args.command == "stats":
        show_stats()
