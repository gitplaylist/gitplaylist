from validate_email import validate_email
import zxcvbn

from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from app import db, login_manager
from models.oauth import GithubAccessToken, SpotifyAccessToken
from exceptions import ValidationError


class User(db.Model, UserMixin):
    """Represent a user model."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    github_accesstoken = db.relationship(GithubAccessToken, uselist=False, back_populates="user")
    spotify_accesstoken = db.relationship(SpotifyAccessToken, uselist=False, back_populates="user")

    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, email, password=None):
        self.email = email
        if password:
            self.password_hash = password

    def __repr__(self):
        return '<User %r>' % (self.email)

    def verify_password(self, password):
        """Check if the user's password is right."""
        if self.password_hash:
            return pwd_context.verify(password, self.password_hash)
        else:
            return False

    @validates('email')
    def validate_email(self, _, email):
        """Validate the email."""
        if not validate_email(email):
            raise ValidationError("Invaild email")
        return email

    @validates('password_hash')
    def validate_password(self, _, password):
        """Validate the password if this is valid."""
        password_entropy = zxcvbn.password_strength(password)['entropy']
        if password_entropy < 20:
            raise ValidationError("Password too weak")
        password_hash = pwd_context.encrypt(password)
        return password_hash


@login_manager.user_loader
def load_user(user_id):
    """Load a user with the user id."""
    return User.query.get(user_id)
