# Quiz model - for storing quiz details
# Took a while to figure out the date handling

from models import db
from datetime import datetime

class Quiz(db.Model):
    """Quiz model for storing quiz related details"""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False, default=datetime.now().date)
    time_duration = db.Column(db.String(5), nullable=False)  # Format: HH:MM
    remarks = db.Column(db.Text, nullable=True)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Quiz {self.id} for Chapter {self.chapter_id}>'