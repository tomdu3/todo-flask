from config import db
from sqlalchemy.sql import func
import bcrypt


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
        )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
        )
    
    def __repr__(self):
        return f'<User {self.username} {self.id}'

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, plaintext_password):
        if not isinstance(plaintext_password, str):
            raise TypeError("Password must be a string")

        # Correcting how password hashing is done
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed_password.decode('utf-8')


    def check_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self._password.encode('utf-8'))