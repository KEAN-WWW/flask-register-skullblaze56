from application.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Explicitly name the table
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @classmethod
    def create(cls, email, password):
        """Create a new user"""
        return cls(email=email, password=password)

    def __repr__(self):
        return f"<User {self.email}>" 