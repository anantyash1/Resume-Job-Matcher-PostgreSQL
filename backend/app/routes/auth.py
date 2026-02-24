# # routes/auth.py

# from datetime import timedelta
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from ..database import get_db
# from ..models import User
# from ..schemas import UserCreate, UserLogin, Token, User as UserSchema
# from ..auth import (
#     verify_password, 
#     get_password_hash, 
#     create_access_token,
#     get_current_user
# )
# from ..config import get_settings

# router = APIRouter(prefix="/auth", tags=["authentication"])
# settings = get_settings()

# @router.post("/register", response_model=UserSchema)
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     """Register a new user"""
    
#     # Check if user already exists
#     db_user = db.query(User).filter(
#         (User.email == user.email) | (User.username == user.username)
#     ).first()
    
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email or username already registered"
#         )
    
#     # Create new user
#     hashed_password = get_password_hash(user.password)
#     new_user = User(
#         email=user.email,
#         username=user.username,
#         hashed_password=hashed_password
#     )
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return new_user

# @router.post("/login", response_model=Token)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     """Login and get access token"""
    
#     db_user = db.query(User).filter(User.username == user.username).first()
    
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     # Create access token
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": db_user.username},
#         expires_delta=access_token_expires
#     )
    
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/me", response_model=UserSchema)
# def get_current_user_info(current_user: User = Depends(get_current_user)):
#     """Get current user information"""
#     return current_user



from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token, User as UserSchema
from ..auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from ..config import get_settings

router = APIRouter(prefix="/auth", tags=["authentication"])
settings = get_settings()


@router.post("/register", response_model=UserSchema, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""

    # Check if user exists
    existing = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user