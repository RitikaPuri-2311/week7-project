from app.database import Base, engine
from app.models import Role, User

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)