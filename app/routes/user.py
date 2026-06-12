from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.utils.password import hash_password

from app.schemas import UserLogin
from app.utils.password import verify_password

from datetime import datetime
from app.mongodb import activity_collection

from fastapi import Query

router = APIRouter(tags=["Users"])


@router.post("/register", status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role_id=user.role_id
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    # Log activity to MongoDB
    activity_collection.insert_one({
    "user_id": db_user.id,
    "event": "login",
    "timestamp": datetime.utcnow()
})


    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "name": db_user.name
    }

@router.post("/logout")
def logout():
    
    # Log logout activity in MongoDB
    activity_collection.insert_one({
        "event": "logout",
        "timestamp": datetime.utcnow()
    })

    return {
        "message": "Logout successful"
    }

from datetime import datetime
from app.mongodb import activity_collection

@router.get("/me")
def get_current_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Log activity
    activity_collection.insert_one({
        "user_id": user.id,
        "event": "view_profile",
        "timestamp": datetime.utcnow()
    })

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role_id": user.role_id,
        "is_active": user.is_active
    }