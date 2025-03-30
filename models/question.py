# Question model - for storing quiz questions and options
# Struggled with storing multiple choice options efficiently

from models import db

class Question(db.Model):
    """Question model for storing question details"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text, nullable=False)
    option4 = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4
    
    def __repr__(self):
        return f'<Question {self.id} for Quiz {self.quiz_id}>'