from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file, abort
from flask_login import login_required, current_user
from .models import db, User, Course, Lesson, Bookmark

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
    full_course_desc = request.form.get('course-desc')
    course_type = request.form.get('course_type')
    skill_level = request.form.get('skill_level')
    course_thumbnail = request.files.get('thumbnail-course')

    if not short_course_desc or not full_course_desc:
        flash("Course Requires Description", "error")

    if not course_title:
        flash("Course Requires Title", "error")
    
    if not course_type or not skill_level:
        flash("Course Requires Course Type and Skill Level", "error")

    if not course_thumbnail:
        image_data = None
        image_mime_type = None

    else:
        image_data = course_thumbnail.read()
        image_mime_type = course_thumbnail.mimetype

    course = Course(
            creator=current_user.user_id, 
            title=course_title, 
            short_desc=short_course_desc,
            full_desc=full_course_desc,
            course_type=course_type,
            skill_level=skill_level,
            thumbnail=image_data, 
            image_mime_type=image_mime_type
            )

    db.session.add(course)
    db.session.commit()

    flash("Course Created!", "success")
    return redirect(url_for("pages.dashboard"))

@pages.route('/submit_lesson', methods=['POST'])
def submit_lesson():
    lesson_title = request.form.get('lesson-title')
    short_lesson_desc = request.form.get('short-lesson-desc')
    lesson_thumbnail = request.files.get('thumbnail-lesson')

    video = request.files.get('video')
    document = request.files.get('document')
    file = request.files.get('file')

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

