# User controller - handles all user functionalities
# Last updated: 2025-03-30 11:32:10
# Author: kharramahendra

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Subject, Chapter, Quiz, Question, Score
from datetime import datetime
from functools import wraps

user = Blueprint('user', __name__)

# User authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with stats and recent quizzes"""
    # Get the current user
    current_user = User.query.get(session['user_id'])
    
    # Get user's recent scores
    recent_scores = Score.query.filter_by(user_id=current_user.id)\
                    .order_by(Score.time_stamp_of_attempt.desc())\
                    .limit(5)\
                    .all()
    
    # Get available subjects
    subjects = Subject.query.all()
    
    return render_template('user/dashboard.html', 
                          user=current_user,
                          recent_scores=recent_scores,
                          subjects=subjects)

@user.route('/subjects')
@login_required
def subjects():
    """List all available subjects"""
    subjects = Subject.query.all()
    return render_template('user/subjects.html', subjects=subjects)

@user.route('/subjects/<int:subject_id>/chapters')
@login_required
def chapters(subject_id):
    """List all chapters for a subject"""
    subject = Subject.query.get_or_404(subject_id)
    return render_template('user/chapters.html', subject=subject, chapters=subject.chapters)

@user.route('/chapters/<int:chapter_id>/quizzes')
@login_required
def quizzes(chapter_id):
    """List all quizzes for a chapter"""
    chapter = Chapter.query.get_or_404(chapter_id)
    current_user = User.query.get(session['user_id'])
    
    # Get attempted quizzes to show scores
    attempted_quizzes = {}
    scores = Score.query.filter_by(user_id=current_user.id).all()
    for score in scores:
        attempted_quizzes[score.quiz_id] = score
    
    return render_template('user/quizzes.html', 
                          chapter=chapter, 
                          quizzes=chapter.quizzes,
                          attempted_quizzes=attempted_quizzes)

@user.route('/quizzes/<int:quiz_id>/take')
@login_required
def take_quiz(quiz_id):
    """Take a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    
    if not questions:
        flash('This quiz has no questions yet', 'warning')
        return redirect(url_for('user.quizzes', chapter_id=quiz.chapter_id))
    
    # Store quiz start time
    session['quiz_start_time'] = datetime.now().timestamp()
    session['quiz_id'] = quiz_id
    
    return render_template('user/take_quiz.html', quiz=quiz, questions=questions)

@user.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """Submit a quiz and calculate score"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    
    if 'quiz_id' not in session or session['quiz_id'] != quiz_id:
        flash('Invalid quiz submission', 'danger')
        return redirect(url_for('user.dashboard'))
    
    # Calculate score
    total_scored = 0
    total_questions = len(questions)
    
    for question in questions:
        answer = request.form.get(f'question_{question.id}')
        if answer and int(answer) == question.correct_option:
            total_scored += 1
    
    # Save score
    score = Score(
        quiz_id=quiz_id,
        user_id=session['user_id'],
        time_stamp_of_attempt=datetime.now(),
        total_scored=total_scored,
        total_questions=total_questions
    )
    db.session.add(score)
    db.session.commit()
    
    # Clear quiz session data
    session.pop('quiz_start_time', None)
    session.pop('quiz_id', None)
    
    flash('Quiz submitted successfully', 'success')
    return redirect(url_for('user.quiz_result', score_id=score.id))

@user.route('/results/<int:score_id>')
@login_required
def quiz_result(score_id):
    """Show quiz result"""
    score = Score.query.get_or_404(score_id)
    
    # Verify that the score belongs to the current user
    if score.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('user.dashboard'))
    
    quiz = score.quiz
    
    return render_template('user/quiz_result.html', score=score, quiz=quiz)

@user.route('/history')
@login_required
def history():
    """Show user's quiz history"""
    current_user = User.query.get(session['user_id'])
    scores = Score.query.filter_by(user_id=current_user.id)\
             .order_by(Score.time_stamp_of_attempt.desc())\
             .all()
    
    return render_template('user/history.html', scores=scores)