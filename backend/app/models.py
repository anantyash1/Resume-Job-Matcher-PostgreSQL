from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_active = Column(Boolean, default=True)
    
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")


class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    description = Column(Text)
    website = Column(String(500))
    industry = Column(String(100))
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_hr = Column(Boolean, default=True)
    
    jobs = relationship("Job", back_populates="company_rel", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="company", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), index=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    salary_range = Column(String(100))
    job_type = Column(String(50), default="Full-time", index=True)
    posted_date = Column(DateTime, default=datetime.utcnow, index=True)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True, index=True)
    
    company_rel = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_job_active_posted', 'is_active', 'posted_date'),
        Index('idx_job_company_active', 'company_id', 'is_active'),
    )


class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(500), nullable=False)
    file_path = Column(String(1000))
    raw_text = Column(Text)
    processed_text = Column(Text)
    skills = Column(Text, default="[]")
    keywords = Column(Text, default="[]")
    uploaded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    user = relationship("User", back_populates="resumes")


class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="pending", index=True)
    cover_letter = Column(Text)
    applied_at = Column(DateTime, default=datetime.utcnow, index=True)
    reviewed_at = Column(DateTime)
    
    user = relationship("User", back_populates="applications")
    resume = relationship("Resume")
    job = relationship("Job", back_populates="applications")
    company = relationship("Company", back_populates="applications")
    
    __table_args__ = (
        Index('idx_app_user_job', 'user_id', 'job_id'),
        Index('idx_app_company_status', 'company_id', 'status'),
    )


class JobMatch(Base):
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    similarity_score = Column(Float, index=True)
    matched_skills = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_match_resume_job', 'resume_id', 'job_id'),
    )