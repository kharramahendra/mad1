# Score model - for storing user quiz scores
# Added total_questions field to calculate percentage easily

from models import db
from datetime import datetime

class Score(db.Model):
    """Score model for storing score details"""
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total_scored = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    
    def percentage_score(self):
        """Calculate the percentage score"""
        if self.total_questions == 0:
            return 0
        return (self.total_scored / self.total_questions) * 100
    
    def __repr__(self):
        return f'<Score {self.id}: {self.total_scored}/{self.total_questions}>'