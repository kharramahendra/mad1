# Subject model - for storing subjects
# Got stuck on how to handle relationship with chapters

from models import db

class Subject(db.Model):
    """Subject model for storing subject related details"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Relationship with chapters - one subject can have many chapters
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Subject {self.name}>'