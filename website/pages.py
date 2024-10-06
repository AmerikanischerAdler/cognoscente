from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file, abort
from flask_login import login_required, current_user
from .models import db, User 

pages = Blueprint("pages", __name__)

@pages.route('/')
@pages.route('/home')
def home():
    return render_template('index.html', user=current_user)

@pages.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@pages.route('/create_course')
def create_course():
    return render_template('create_course.html', user=current_user)

@pages.route('/submit_course', methods=['POST'])
def submit_course():
    course_title = request.form.get('course-title')
    short_course_desc = request.form.get('short-course-desc')
    course_type = request.form.get('course_type')
    skill_level = request.form.get('skill_level')
    thumbnail = request.files.get('thumbnail')

    # DB stuff

    return jsonify({
        'status': 'success', 
        'message': 'Course submitted successfully'
        })

@pages.route('/submit_lesson', methods=['POST'])
def submit_lesson():
    lesson_title = request.form.get('lesson-title')
    short_lesson_desc = request.form.get('short-lesson-desc')
    lesson_thumbnail = request.files.get('thumbnail-lesson')

    # DB stuff

    return jsonify({
        'status': 'success', 
        'message': 'Lesson submitted successfully'
        })

@pages.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@pages.route('/settings')
@login_required
def settings():
    return render_template('settings.html', user=current_user)

@pages.route('/not-settings')
def not_settings():
    return render_template('not_settings.html', user=current_user)

