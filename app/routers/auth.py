from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.utils.security import hash_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

# -------------------------signup------------------------
@router.post("/signup", response_model=User)
def create_user(user_data: User, session: Session = Depends(get_session)):
    # 1. Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hash the password
    hashed_pwd = hash_password(user_data.password)
    user_data.password = hashed_pwd

    # 3. Save to DB
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    
    return user_data



    # ----------------------sign In -----------------------
    # Add these imports at the top of auth.py:
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.security import verify_password, create_access_token
from datetime import timedelta

# ... keep your existing signup code ...

# --- NEW: Login Endpoint ---
@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    # 1. Find the user
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    # 2. Check if user exists AND password is correct
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Create the Token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 4. Return the Token
    return {"access_token": access_token, "token_type": "bearer"}