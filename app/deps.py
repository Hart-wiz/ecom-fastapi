from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.utils.security import SECRET_KEY, ALGORITHM

# 1. Tell FastAPI where to find the login URL (so the lock icon works in docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 2. The Guard Function
def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Check if user actually exists in DB
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if user is None:
        raise credentials_exception
        
    return user