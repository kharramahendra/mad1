# Chapter model - for storing chapters within subjects
# Had to reference Flask docs for the cascade delete behavior

from models import db

class Chapter(db.Model):
    """Chapter model for storing chapter related details"""
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    # Relationship with quizzes - one chapter can have many quizzes
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Chapter {self.name}>'