from app.database import SessionLocal
from app.models import Role

db = SessionLocal()

roles = [
    Role(role_name="Admin"),
    Role(role_name="User")
]

for role in roles:
    existing = db.query(Role).filter(
        Role.role_name == role.role_name
    ).first()

    if not existing:
        db.add(role)

db.commit()
db.close()

print("Roles added successfully!")