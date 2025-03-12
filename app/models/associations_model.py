from app.config import db
from app.models.user_model import User
from app.models.password_model import Password

User.password = db.relationship(
    "Password", 
    backref="user", 
    uselist=False, 
    cascade="all, delete-orphan"
)


