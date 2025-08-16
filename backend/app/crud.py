from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import CVSession, User
from typing import Optional, Dict, Any, List
import json

class CVSessionCRUD:
    """CRUD operations for CV sessions."""
    
    @staticmethod
    def create_session(db: Session, session_id: str, cv_text: str, cv_file_type: str, cv_file_path: str = None) -> CVSession:
        """Create a new CV session."""
        db_session = CVSession(
            id=session_id,
            cv_text=cv_text,
            cv_file_type=cv_file_type,
            cv_file_path=cv_file_path
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[CVSession]:
        """Get a CV session by ID."""
        return db.query(CVSession).filter(CVSession.id == session_id).first()
    
    @staticmethod
    def update_analysis(
        db: Session, 
        session_id: str, 
        job_title: str,
        job_description: str,
        original_score: int,
        missing_skills: List[str],
        strengths: List[str],
        experience_gaps: List[str],
        recommendations: List[str],
        summary: str
    ) -> Optional[CVSession]:
        """Update session with analysis results."""
        session = db.query(CVSession).filter(CVSession.id == session_id).first()
        if session:
            session.job_title = job_title
            session.job_description = job_description
            session.original_score = original_score
            session.missing_skills = missing_skills
            session.strengths = strengths
            session.experience_gaps = experience_gaps
            session.recommendations = recommendations
            session.summary = summary
            db.commit()
            db.refresh(session)
        return session
    
    @staticmethod
    def update_enhancement(
        db: Session,
        session_id: str,
        additional_info: str,
        new_score: int,
        improvement_suggestions: Dict[str, Any],
        enhanced_cv_path: str
    ) -> Optional[CVSession]:
        """Update session with enhancement results."""
        session = db.query(CVSession).filter(CVSession.id == session_id).first()
        if session:
            session.additional_info = additional_info
            session.new_score = new_score
            session.improvement_suggestions = improvement_suggestions
            session.enhanced_cv_path = enhanced_cv_path
            db.commit()
            db.refresh(session)
        return session
    
    @staticmethod
    def get_all_sessions(db: Session, limit: int = 100) -> List[CVSession]:
        """Get all CV sessions (for admin purposes)."""
        return db.query(CVSession).order_by(CVSession.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_filtered_sessions(
        db: Session, 
        limit: int = 100, 
        skip: int = 0,
        job_title: str = None,
        min_score: int = None,
        max_score: int = None,
        file_type: str = None
    ) -> List[CVSession]:
        """Get filtered CV sessions with pagination."""
        query = db.query(CVSession)
        
        # Apply filters
        if job_title:
            query = query.filter(CVSession.job_title.ilike(f"%{job_title}%"))
        if min_score is not None:
            query = query.filter(CVSession.original_score >= min_score)
        if max_score is not None:
            query = query.filter(CVSession.original_score <= max_score)
        if file_type:
            query = query.filter(CVSession.cv_file_type == file_type)
        
        return query.order_by(CVSession.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_sessions_count(db: Session) -> int:
        """Get total count of CV sessions."""
        return db.query(CVSession).count()
    
    @staticmethod
    def get_comprehensive_stats(db: Session) -> Dict[str, Any]:
        """Get comprehensive statistics about CV sessions."""
        from sqlalchemy import func, text
        from datetime import datetime, timedelta
        
        # Basic counts
        total_sessions = db.query(CVSession).count()
        analyzed_sessions = db.query(CVSession).filter(CVSession.original_score.isnot(None)).count()
        enhanced_sessions = db.query(CVSession).filter(CVSession.enhanced_cv_path.isnot(None)).count()
        
        # Score statistics
        score_stats = db.query(
            func.avg(CVSession.original_score).label('avg_original'),
            func.avg(CVSession.new_score).label('avg_enhanced'),
            func.max(CVSession.original_score).label('max_original'),
            func.min(CVSession.original_score).label('min_original'),
            func.max(CVSession.new_score - CVSession.original_score).label('max_improvement')
        ).filter(CVSession.original_score.isnot(None)).first()
        
        # File type distribution
        file_type_stats = db.query(
            CVSession.cv_file_type,
            func.count(CVSession.cv_file_type).label('count')
        ).group_by(CVSession.cv_file_type).all()
        
        file_type_distribution = {stat.cv_file_type: stat.count for stat in file_type_stats}
        
        # Top job titles
        job_title_stats = db.query(
            CVSession.job_title,
            func.count(CVSession.job_title).label('count')
        ).filter(CVSession.job_title.isnot(None)).group_by(CVSession.job_title).order_by(func.count(CVSession.job_title).desc()).limit(10).all()
        
        top_job_titles = [{"title": stat.job_title, "count": stat.count} for stat in job_title_stats]
        
        # Recent activity
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        jobs_last_7_days = db.query(CVSession).filter(CVSession.created_at >= seven_days_ago).count()
        jobs_last_30_days = db.query(CVSession).filter(CVSession.created_at >= thirty_days_ago).count()
        
        # Performance metrics
        high_performing_jobs = db.query(CVSession).filter(CVSession.original_score >= 80).count()
        low_performing_jobs = db.query(CVSession).filter(CVSession.original_score < 50).count()
        most_improved_jobs = db.query(CVSession).filter(
            (CVSession.new_score - CVSession.original_score) >= 20
        ).count()
        
        return {
            "total_sessions": total_sessions,
            "analyzed_sessions": analyzed_sessions,
            "enhanced_sessions": enhanced_sessions,
            "avg_original_score": round(score_stats.avg_original, 2) if score_stats.avg_original else 0,
            "avg_enhanced_score": round(score_stats.avg_enhanced, 2) if score_stats.avg_enhanced else 0,
            "avg_improvement": round((score_stats.avg_enhanced or 0) - (score_stats.avg_original or 0), 2),
            "max_original_score": score_stats.max_original or 0,
            "min_original_score": score_stats.min_original or 0,
            "max_improvement": score_stats.max_improvement or 0,
            "file_type_distribution": file_type_distribution,
            "top_job_titles": top_job_titles,
            "jobs_last_7_days": jobs_last_7_days,
            "jobs_last_30_days": jobs_last_30_days,
            "high_performing_jobs": high_performing_jobs,
            "low_performing_jobs": low_performing_jobs,
            "most_improved_jobs": most_improved_jobs
        }
    
    @staticmethod
    def delete_session(db: Session, session_id: str) -> bool:
        """Delete a CV session."""
        session = db.query(CVSession).filter(CVSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
            return True
        return False

class UserCRUD:
    """CRUD operations for users."""
    
    @staticmethod
    def create_user(db: Session, email: str = None, name: str = None) -> User:
        """Create a new user."""
        db_user = User(email=email, name=name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
