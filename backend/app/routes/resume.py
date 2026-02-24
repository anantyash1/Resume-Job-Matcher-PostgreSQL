# import os
# import json
# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
# from sqlalchemy.orm import Session
# from ..database import get_db
# from ..models import User, Resume
# from ..schemas import ResumeResponse
# from ..auth import get_current_user
# from ..services.resume_parser import ResumeParser
# from ..services.nlp_processor import NLPProcessor


# import os
# import json
# from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
# from sqlalchemy.orm import Session
# from typing import List

# from ..database import get_db
# from ..models import User, Resume
# from ..schemas import ResumeResponse
# from ..auth import get_current_user
# from ..services.resume_parser import ResumeParser
# from ..services.nlp_processor import process_resume_text

# router = APIRouter(prefix="/resume", tags=["resume"])

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# resume_parser = ResumeParser()
# nlp_processor = NLPProcessor()

# @router.post("/upload", response_model=ResumeResponse)
# async def upload_resume(
#     file: UploadFile = File(...),
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """Upload and process resume"""
    
#     # Validate file type
#     allowed_extensions = ['.pdf', '.doc', '.docx', '.png', '.jpg', '.jpeg']
#     file_ext = os.path.splitext(file.filename)[1].lower()
    
#     if file_ext not in allowed_extensions:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
#         )
    
#     # Save file
#     file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    
#     try:
#         with open(file_path, "wb") as buffer:
#             content = await file.read()
#             buffer.write(content)
        
#         # Extract text
#         raw_text = resume_parser.extract_text(file_path, file.filename)
        
#         if not raw_text or len(raw_text) < 50:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Could not extract sufficient text from resume"
#             )
        
#         # Process text
#         processed_text = nlp_processor.preprocess_text(raw_text)
#         skills = nlp_processor.extract_skills(raw_text)
#         keywords = nlp_processor.extract_keywords(raw_text)
        
#         # Save to database
#         resume = Resume(
#             user_id=current_user.id,
#             filename=file.filename,
#             raw_text=raw_text,
#             processed_text=processed_text,
#             skills=json.dumps(skills),
#             keywords=json.dumps(keywords)
#         )
        
#         db.add(resume)
#         db.commit()
#         db.refresh(resume)
        
#         return {
#             "id": resume.id,
#             "filename": resume.filename,
#             "skills": skills,
#             "keywords": keywords,
#             "uploaded_at": resume.uploaded_at
#         }
        
#     except Exception as e:
#         # Clean up file if error
#         if os.path.exists(file_path):
#             os.remove(file_path)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error processing resume: {str(e)}"
#         )

# @router.get("/my-resumes", response_model=list[ResumeResponse])
# def get_my_resumes(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """Get all resumes for current user"""
    
#     resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    
#     return [
#         {
#             "id": r.id,
#             "filename": r.filename,
#             "skills": json.loads(r.skills) if r.skills else [],
#             "keywords": json.loads(r.keywords) if r.keywords else [],
#             "uploaded_at": r.uploaded_at
#         }
#         for r in resumes
#     ]




import os
import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Resume
from ..schemas import ResumeResponse
from ..auth import get_current_user
from ..services.nlp_processor import process_resume_text

router = APIRouter(prefix="/resume", tags=["resume"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_text_from_file(file_path: str, filename: str) -> str:
    """Extract text from uploaded file"""
    ext = os.path.splitext(filename)[1].lower()
    raw_text = ""

    try:
        if ext == ".pdf":
            try:
                import PyPDF2
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        raw_text += page.extract_text() or ""
            except Exception as e:
                print(f"PDF error: {e}")

        elif ext in [".doc", ".docx"]:
            try:
                from docx import Document
                doc = Document(file_path)
                raw_text = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                print(f"DOCX error: {e}")

        elif ext in [".png", ".jpg", ".jpeg"]:
            try:
                import pytesseract
                from PIL import Image
                img = Image.open(file_path)
                raw_text = pytesseract.image_to_string(img)
            except Exception as e:
                print(f"OCR error: {e}")

        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()

    except Exception as e:
        print(f"Error extracting text: {e}")

    return raw_text.strip()


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a resume"""

    # Validate file type
    allowed_extensions = [".pdf", ".doc", ".docx", ".png", ".jpg", ".jpeg", ".txt"]
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_ext}' not allowed. Allowed: {allowed_extensions}"
        )

    # Save file to disk
    safe_filename = f"{current_user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Extract text
    raw_text = extract_text_from_file(file_path, file.filename)

    if not raw_text:
        raw_text = f"Resume file: {file.filename}"

    # Process NLP - extract ONLY technical skills/keywords
    try:
        processed = process_resume_text(raw_text)
        skills = processed.get("skills", [])
        keywords = processed.get("keywords", [])
        processed_text = processed.get("processed_text", raw_text)
    except Exception as e:
        print(f"NLP processing error: {e}")
        skills = []
        keywords = []
        processed_text = raw_text

    # Save to database
    try:
        resume = Resume(
            user_id=current_user.id,
            filename=file.filename,
            file_path=file_path,
            raw_text=raw_text,
            processed_text=processed_text,
            skills=json.dumps(skills),
            keywords=json.dumps(keywords)
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return ResumeResponse(
        id=resume.id,
        filename=resume.filename,
        uploaded_at=resume.uploaded_at,
        skills=skills,
        keywords=keywords
    )


@router.get("/my-resumes", response_model=List[ResumeResponse])
def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for current user"""

    resumes = db.query(Resume).filter(
        Resume.user_id == current_user.id
    ).order_by(Resume.uploaded_at.desc()).all()

    result = []
    for r in resumes:
        try:
            skills = json.loads(r.skills) if r.skills else []
        except Exception:
            skills = []
        try:
            keywords = json.loads(r.keywords) if r.keywords else []
        except Exception:
            keywords = []

        result.append(ResumeResponse(
            id=r.id,
            filename=r.filename,
            uploaded_at=r.uploaded_at,
            skills=skills,
            keywords=keywords
        ))

    return result


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resume"""

    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Delete file from disk
    if resume.file_path and os.path.exists(resume.file_path):
        try:
            os.remove(resume.file_path)
        except Exception:
            pass

    db.delete(resume)
    db.commit()

    return {"message": "Resume deleted successfully"}