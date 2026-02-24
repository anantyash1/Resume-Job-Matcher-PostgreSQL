# import json
# from fastapi import APIRouter, Depends, HTTPException, status, Query
# from sqlalchemy.orm import Session
# from ..database import get_db
# from ..models import User, Resume, Job, JobMatch
# from ..schemas import JobMatchResponse
# from ..auth import get_current_user
# from ..services.job_matcher import JobMatcher

# router = APIRouter(prefix="/jobs", tags=["jobs"])

# job_matcher = JobMatcher()

# @router.get("/recommendations", response_model=list[JobMatchResponse])
# def get_job_recommendations(
#     resume_id: int = Query(..., description="Resume ID to match against"),
#     top_n: int = Query(10, ge=1, le=50, description="Number of recommendations"),
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """Get job recommendations for a resume"""
    
#     # Verify resume belongs to user
#     resume = db.query(Resume).filter(
#         Resume.id == resume_id,
#         Resume.user_id == current_user.id
#     ).first()
    
#     if not resume:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Resume not found"
#         )
    
#     # Get all jobs
#     jobs = db.query(Job).all()
    
#     if not jobs:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No jobs available in database"
#         )
    
#     # Convert to dict format
#     jobs_data = [
#         {
#             'id': job.id,
#             'title': job.title,
#             'company': job.company,
#             'location': job.location,
#             'description': job.description,
#             'requirements': job.requirements or '',
#             'salary_range': job.salary_range,
#             'job_type': job.job_type,
#             'posted_date': job.posted_date
#         }
#         for job in jobs
#     ]
    
#     # Get resume data
#     resume_skills = json.loads(resume.skills) if resume.skills else []
    
#     # Match jobs
#     matches = job_matcher.match_jobs(
#         resume_text=resume.processed_text or resume.raw_text,
#         resume_skills=resume_skills,
#         jobs=jobs_data,
#         top_n=top_n
#     )
    
#     # Save matches to database
#     for match in matches:
#         job_match = JobMatch(
#             resume_id=resume.id,
#             job_id=match['job']['id'],
#             similarity_score=match['similarity_score'],
#             matched_skills=json.dumps(match['matched_skills'])
#         )
#         db.merge(job_match)
    
#     db.commit()
    
#     # Format response
#     results = []
#     for match in matches:
#         job = match['job']
#         results.append({
#             'id': job['id'],
#             'title': job['title'],
#             'company': job['company'],
#             'location': job['location'],
#             'description': job['description'],
#             'requirements': job['requirements'],
#             'salary_range': job['salary_range'],
#             'job_type': job['job_type'],
#             'posted_date': job['posted_date'],
#             'similarity_score': match['similarity_score'],
#             'matched_skills': match['matched_skills']
#         })
    
#     return results




# import json
# from datetime import datetime
# from fastapi import APIRouter, Depends, HTTPException, status, Query
# from sqlalchemy.orm import Session
# from typing import List

# from ..database import get_db
# from ..models import User, Resume, Job, JobMatch
# from ..schemas import JobMatchResponse
# from ..auth import get_current_user
# from ..services.job_matcher import JobMatcher
# from ..services.nlp_processor import extract_skills_from_text

# router = APIRouter(prefix="/jobs", tags=["jobs"])
# job_matcher = JobMatcher()


# @router.get("/recommendations", response_model=List[JobMatchResponse])
# def get_job_recommendations(
#     resume_id: int = Query(...),
#     top_n: int = Query(10, ge=1, le=50),
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """Get job recommendations. Includes HR-created jobs + seeded jobs."""

#     resume = db.query(Resume).filter(
#         Resume.id == resume_id,
#         Resume.user_id == current_user.id
#     ).first()

#     if not resume:
#         raise HTTPException(status_code=404, detail="Resume not found")

#     # Get ALL active jobs (both seeded and HR-created)
#     jobs = db.query(Job).filter(Job.is_active == True).all()

#     if not jobs:
#         raise HTTPException(status_code=404, detail="No active jobs in database")

#     jobs_data = [{
#         'id': j.id,
#         'title': j.title,
#         'company': j.company,
#         'company_id': j.company_id,
#         'location': j.location,
#         'description': j.description or '',
#         'requirements': j.requirements or '',
#         'salary_range': j.salary_range,
#         'job_type': j.job_type,
#         'posted_date': j.posted_date
#     } for j in jobs]

#     resume_skills = json.loads(resume.skills) if resume.skills else []
#     resume_text = resume.processed_text or resume.raw_text or ""

#     # Match using 85% skill threshold
#     try:
#         matches = job_matcher.match_jobs(
#             resume_text=resume_text,
#             resume_skills=resume_skills,
#             jobs=jobs_data,
#             top_n=top_n
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Matching error: {str(e)}")

#     # Save matches to database
#     for match in matches:
#         try:
#             existing = db.query(JobMatch).filter(
#                 JobMatch.resume_id == resume.id,
#                 JobMatch.job_id == match['job']['id']
#             ).first()

#             if existing:
#                 existing.similarity_score = match['similarity_score']
#                 existing.matched_skills = json.dumps(match['matched_skills'])
#             else:
#                 db.add(JobMatch(
#                     resume_id=resume.id,
#                     job_id=match['job']['id'],
#                     similarity_score=match['similarity_score'],
#                     matched_skills=json.dumps(match['matched_skills'])
#                 ))
#         except Exception:
#             pass

#     try:
#         db.commit()
#     except Exception:
#         db.rollback()

#     # Build response
#     return [{
#         'id': m['job']['id'],
#         'title': m['job']['title'],
#         'company': m['job']['company'],
#         'location': m['job']['location'],
#         'description': m['job']['description'],
#         'requirements': m['job']['requirements'],
#         'salary_range': m['job']['salary_range'],
#         'job_type': m['job']['job_type'],
#         'posted_date': m['job']['posted_date'],
#         'similarity_score': m['similarity_score'],
#         'matched_skills': m['matched_skills']
#     } for m in matches]




import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Resume, Job, JobMatch
from ..schemas import JobMatchResponse
from ..auth import get_current_user
from ..services.job_matcher import JobMatcher

router = APIRouter(prefix="/jobs", tags=["jobs"])
job_matcher = JobMatcher()


@router.get("/recommendations", response_model=List[JobMatchResponse])
def get_job_recommendations(
    resume_id: int = Query(...),
    top_n: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get job recommendations from DATABASE (includes seeded + HR-created jobs).
    NO JSON file reading here - everything from database.
    """

    # Verify resume ownership
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Get ALL active jobs from DATABASE (seeded + newly created by HR)
    jobs = db.query(Job).filter(Job.is_active == True).all()

    if not jobs:
        raise HTTPException(status_code=404, detail="No active jobs available")

    print(f"Found {len(jobs)} active jobs in database for matching")

    # Convert to dict format for matcher
    jobs_data = [{
        'id': j.id,
        'title': j.title,
        'company': j.company,
        'company_id': j.company_id,
        'location': j.location,
        'description': j.description or '',
        'requirements': j.requirements or '',
        'salary_range': j.salary_range,
        'job_type': j.job_type,
        'posted_date': j.posted_date
    } for j in jobs]

    # Get resume skills and text
    resume_skills = json.loads(resume.skills) if resume.skills else []
    resume_text = resume.processed_text or resume.raw_text or ""

    # Match jobs using 85% technical skill threshold
    try:
        matches = job_matcher.match_jobs(
            resume_text=resume_text,
            resume_skills=resume_skills,
            jobs=jobs_data,
            top_n=top_n
        )
        print(f"Matched {len(matches)} jobs for user")
    except Exception as e:
        print(f"Matching error: {e}")
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

    # Save matches to database
    for match in matches:
        try:
            existing = db.query(JobMatch).filter(
                JobMatch.resume_id == resume.id,
                JobMatch.job_id == match['job']['id']
            ).first()

            if existing:
                existing.similarity_score = match['similarity_score']
                existing.matched_skills = json.dumps(match['matched_skills'])
            else:
                db.add(JobMatch(
                    resume_id=resume.id,
                    job_id=match['job']['id'],
                    similarity_score=match['similarity_score'],
                    matched_skills=json.dumps(match['matched_skills'])
                ))
        except Exception:
            pass

    try:
        db.commit()
    except Exception:
        db.rollback()

    # Format response
    return [{
        'id': m['job']['id'],
        'title': m['job']['title'],
        'company': m['job']['company'],
        'location': m['job']['location'],
        'description': m['job']['description'],
        'requirements': m['job']['requirements'],
        'salary_range': m['job']['salary_range'],
        'job_type': m['job']['job_type'],
        'posted_date': m['job']['posted_date'],
        'similarity_score': m['similarity_score'],
        'matched_skills': m['matched_skills']
    } for m in matches]