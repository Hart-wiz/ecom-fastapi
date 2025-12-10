from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.product import Product
from typing import List
from app.deps import get_current_user
from app.models.user import User


# This groups all our product URLs together
router = APIRouter(prefix="/products", tags=["Products"])

# 1. The "Create" Endpoint (POST)
@router.post("/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session),current_user: User = Depends(get_current_user)):
    session.add(product)      # 1. Stage the new product
    session.commit()          # 2. Save it to the DB
    session.refresh(product)  # 3. Get the new ID back from the DB
    return product

# 2. The "Read All" Endpoint (GET)
@router.get("/", response_model=List[Product])
def read_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products