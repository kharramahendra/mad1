# Admin controller - handles all admin functionalities
# Last updated: 2025-03-30 11:32:10
# Author: kharramahendra

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
from functools import wraps

admin = Blueprint('admin', __name__)

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('You need to be logged in as an admin to access this page', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with stats and charts"""
    # Get counts for dashboard
    user_count = User.query.filter_by(is_admin=False).count()
    subject_count = Subject.query.count()
    quiz_count = Quiz.query.count()
    question_count = Question.query.count()
    
    # Get recent users
    recent_users = User.query.filter_by(is_admin=False).order_by(User.id.desc()).limit(5).all()
    
    # Get recent quizzes
    recent_quizzes = Quiz.query.order_by(Quiz.id.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count,
                          subject_count=subject_count,
                          quiz_count=quiz_count,
                          question_count=question_count,
                          recent_users=recent_users,
                          recent_quizzes=recent_quizzes)

# Subject management
@admin.route('/subjects')
@admin_required
def subjects():
    """List all subjects"""
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin.route('/subjects/add', methods=['GET', 'POST'])
@admin_required
def add_subject():
    """Add a new subject"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Basic validation
        if not name:
            flash('Subject name is required', 'danger')
            return redirect(url_for('admin.add_subject'))
        
        # Create subject
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        
        flash('Subject added successfully', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/add_subject.html')

@admin.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_subject(subject_id):
    """Edit a subject"""
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Subject name is required', 'danger')
            return redirect(url_for('admin.edit_subject', subject_id=subject_id))
        
        subject.name = name
        subject.description = description
        db.session.commit()
        
        flash('Subject updated successfully', 'success')
        return redirect(url_for('admin.subjects'))
    
    return render_template('admin/edit_subject.html', subject=subject)

@admin.route('/subjects/<int:subject_id>/delete')
@admin_required
def delete_subject(subject_id):
    """Delete a subject"""
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    
    flash('Subject deleted successfully', 'success')
    return redirect(url_for('admin.subjects'))

# Chapter management
@admin.route('/subjects/<int:subject_id>/chapters')
@admin_required
def chapters(subject_id):
    """List all chapters for a subject"""
    subject = Subject.query.get_or_404(subject_id)
    return render_template('admin/chapters.html', subject=subject, chapters=subject.chapters)

@admin.route('/subjects/<int:subject_id>/chapters/add', methods=['GET', 'POST'])
@admin_required
def add_chapter(subject_id):
    """Add a new chapter to a subject"""
    subject = Subject.query.get_or_404(subject_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Chapter name is required', 'danger')
            return redirect(url_for('admin.add_chapter', subject_id=subject_id))
        
        chapter = Chapter(name=name, description=description, subject_id=subject_id)
        db.session.add(chapter)
        db.session.commit()
        
        flash('Chapter added successfully', 'success')
        return redirect(url_for('admin.chapters', subject_id=subject_id))
    
    return render_template('admin/add_chapter.html', subject=subject)

@admin.route('/chapters/<int:chapter_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_chapter(chapter_id):
    """Edit a chapter"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Chapter name is required', 'danger')
            return redirect(url_for('admin.edit_chapter', chapter_id=chapter_id))
        
        chapter.name = name
        chapter.description = description
        db.session.commit()
        
        flash('Chapter updated successfully', 'success')
        return redirect(url_for('admin.chapters', subject_id=chapter.subject_id))
    
    return render_template('admin/edit_chapter.html', chapter=chapter)

@admin.route('/chapters/<int:chapter_id>/delete')
@admin_required
def delete_chapter(chapter_id):
    """Delete a chapter"""
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id
    
    db.session.delete(chapter)
    db.session.commit()
    
    flash('Chapter deleted successfully', 'success')
    return redirect(url_for('admin.chapters', subject_id=subject_id))

# Quiz management
@admin.route('/chapters/<int:chapter_id>/quizzes')
@admin_required
def quizzes(chapter_id):
    """List all quizzes for a chapter"""
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('admin/quizzes.html', chapter=chapter, quizzes=chapter.quizzes)

@admin.route('/chapters/<int:chapter_id>/quizzes/add', methods=['GET', 'POST'])
@admin_required
def add_quiz(chapter_id):
    """Add a new quiz to a chapter"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if request.method == 'POST':
        date_of_quiz_str = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        
        try:
            date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for('admin.add_quiz', chapter_id=chapter_id))
        
        if not time_duration or not time_duration.strip():
            flash('Time duration is required', 'danger')
            return redirect(url_for('admin.add_quiz', chapter_id=chapter_id))
        
        quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks
        )
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz added successfully', 'success')
        return redirect(url_for('admin.quizzes', chapter_id=chapter_id))
    
    return render_template('admin/add_quiz.html', chapter=chapter)

@admin.route('/quizzes/<int:quiz_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_quiz(quiz_id):
    """Edit a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        date_of_quiz_str = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        
        try:
            date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for('admin.edit_quiz', quiz_id=quiz_id))
        
        if not time_duration or not time_duration.strip():
            flash('Time duration is required', 'danger')
            return redirect(url_for('admin.edit_quiz', quiz_id=quiz_id))
        
        quiz.date_of_quiz = date_of_quiz
        quiz.time_duration = time_duration
        quiz.remarks = remarks
        db.session.commit()
        
        flash('Quiz updated successfully', 'success')
        return redirect(url_for('admin.quizzes', chapter_id=quiz.chapter_id))
    
    return render_template('admin/edit_quiz.html', quiz=quiz)

@admin.route('/quizzes/<int:quiz_id>/delete')
@admin_required
def delete_quiz(quiz_id):
    """Delete a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id
    
    db.session.delete(quiz)
    db.session.commit()
    
    flash('Quiz deleted successfully', 'success')
    return redirect(url_for('admin.quizzes', chapter_id=chapter_id))

# Question management
@admin.route('/quizzes/<int:quiz_id>/questions')
@admin_required
def questions(quiz_id):
    """List all questions for a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/questions.html', quiz=quiz, questions=quiz.questions)

@admin.route('/quizzes/<int:quiz_id>/questions/add', methods=['GET', 'POST'])
@admin_required
def add_question(quiz_id):
    """Add a new question to a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')
        
        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash('All fields are required', 'danger')
            return redirect(url_for('admin.add_question', quiz_id=quiz_id))
        
        question = Question(
            quiz_id=quiz_id,
            question_statement=question_statement,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=int(correct_option)
        )
        db.session.add(question)
        db.session.commit()
        
        flash('Question added successfully', 'success')
        return redirect(url_for('admin.questions', quiz_id=quiz_id))
    
    return render_template('admin/add_question.html', quiz=quiz)

@admin.route('/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    """Edit a question"""
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        question_statement = request.form.get('question_statement')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correct_option')
        
        if not question_statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
            flash('All fields are required', 'danger')
            return redirect(url_for('admin.edit_question', question_id=question_id))
        
        question.question_statement = question_statement
        question.option1 = option1
        question.option2 = option2
        question.option3 = option3
        question.option4 = option4
        question.correct_option = int(correct_option)
        db.session.commit()
        
        flash('Question updated successfully', 'success')
        return redirect(url_for('admin.questions', quiz_id=question.quiz_id))
    
    return render_template('admin/edit_question.html', question=question)

@admin.route('/questions/<int:question_id>/delete')
@admin_required
def delete_question(question_id):
    """Delete a question"""
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    
    db.session.delete(question)
    db.session.commit()
    
    flash('Question deleted successfully', 'success')
    return redirect(url_for('admin.questions', quiz_id=quiz_id))

# User management
@admin.route('/users')
@admin_required
def users():
    """List all users"""
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)