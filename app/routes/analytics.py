from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Role
from app.mongodb import activity_collection

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)
@router.get("/users")
def analytics_users(db: Session = Depends(get_db)):

    total_users = db.query(User).count()

    active_users = db.query(User).filter(
        User.is_active == True
    ).count()

    roles = db.query(Role).all()

    users_by_role = {}

    for role in roles:
        count = db.query(User).filter(
            User.role_id == role.id
        ).count()

        users_by_role[role.role_name] = count

    return {
        "total_users": total_users,
        "active_users": active_users,
        "users_by_role": users_by_role
    }

@router.get("/activity")
def analytics_activity():

    pipeline = [
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$timestamp"
                    }
                },
                "event_count": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    return list(
        activity_collection.aggregate(pipeline)
    )

@router.get("/logins")
def login_frequency(
    db: Session = Depends(get_db)
):

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    pipeline = [
        {
            "$match": {
                "event": "login",
                "timestamp": {
                    "$gte": seven_days_ago
                }
            }
        },
        {
            "$group": {
                "_id": "$user_id",
                "login_count": {
                    "$sum": 1
                }
            }
        }
    ]

    login_data = list(
        activity_collection.aggregate(pipeline)
    )

    result = []

    for item in login_data:

        user = db.query(User).filter(
            User.id == item["_id"]
        ).first()

        if user:
            result.append({
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "login_count": item["login_count"]
            })

    return result
