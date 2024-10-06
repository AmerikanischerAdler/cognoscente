from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'  

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # Override get_id to take user_id instead of id 
    def get_id(self):
        return str(self.user_id)  

    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    __tablename__ = 'courses'  

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_desc = db.Column(db.String(100), nullable=False)
    full_desc = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.LargeBinary, nullable=True)
    image_mime_type = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    creator = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    lessons = db.relationship("Lesson", backref="course", passive_deletes=True)
    bookmarks = db.relationship("Bookmark", backref="course", passive_deletes=True)

class Lesson(db.Model):
    __tablename__ = 'lessons'  

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.LargeBinary, nullable=True)
    image_mime_type = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    creator = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'  

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    creator = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

