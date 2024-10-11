from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file, abort
from flask_login import login_required, current_user
from .models import db, User, Course, Lesson, Bookmark
import random
import string
import io

pages = Blueprint("pages", __name__)

@pages.route('/')
@pages.route('/home')
def home():
    return render_template('index.html', user=current_user)

@pages.route('/search')
def search():
    query = request.args.get('query')

    courses = Course.query.filter(Course.title.ilike(f'%{query}%') | Course.short_desc.like(f'%{query}%')).all()
    science_courses = Course.query.filter_by(course_type="Science").all()
    tech_courses = Course.query.filter_by(course_type="Technology").all()
    eng_courses = Course.query.filter_by(course_type="Engineering").all()
    math_courses = Course.query.filter_by(course_type="Mathematics").all()
    creators = User.query.filter(User.username.ilike(f'%{query}%')).all()

    return render_template('search_results.html', query=query, courses=courses, creators=creators, user=current_user, math_courses=math_courses, tech_courses=tech_courses, eng_courses=eng_courses, science_courses=science_courses)

@pages.route('/dashboard')
@login_required
def dashboard():
    courses = current_user.courses

    return render_template('dashboard.html', user=current_user, courses=courses)

@pages.route('/explore')
def explore():
    science_courses = Course.query.filter_by(course_type="Science").all()
    tech_courses = Course.query.filter_by(course_type="Technology").all()
    eng_courses = Course.query.filter_by(course_type="Engineering").all()
    math_courses = Course.query.filter_by(course_type="Mathematics").all()

    return render_template('explore.html', user=current_user, math_courses=math_courses, tech_courses=tech_courses, eng_courses=eng_courses, science_courses=science_courses)

@pages.route('/create_course/<course_id>')
def create_course(course_id):
    # For New Course
    if course_id == 0 or course_id == "0":
        # Generates Temporary Course Info to Append Lessons 
        def title_gen(name):
            chars = string.printable
            word = ""

            if name == "title":
                length = 50
            elif name == "short_desc":
                length = 100
            elif name == "full_desc":
                length = 200
            
            for i in range(length):
                word += chars[random.randint(0,len(chars)-1)]
            
            return word

        course_title = title_gen("title")
        short_course_desc = title_gen("short_desc")
        full_course_desc = title_gen("full_desc")

        course_type = "in_progress"
        skill_level = "in_progress"

        image_data = None
        image_mime_type = None

        crs = Course(
                creator=current_user.user_id, 
                title=course_title, 
                short_desc=short_course_desc,
                full_desc=full_course_desc,
                course_type=course_type,
                skill_level=skill_level,
                thumbnail=image_data, 
                image_mime_type=image_mime_type
                )

        db.session.add(crs)
        db.session.commit()

        course = Course.query.filter_by(title=course_title).first()
    
    # For Editing Course
    else:
        course = Course.query.filter_by(id=course_id).first()

    return render_template('create_course.html', user=current_user, course=course)

@pages.route('/get_thumbnail/<int:course_id>')
def get_thumbnail(course_id):
    course = Course.query.get(course_id)
    if course and course.thumbnail and course.image_mime_type:
        return send_file(
            io.BytesIO(course.thumbnail),
            mimetype=course.image_mime_type,
            as_attachment=False,
            download_name=f'course_{course_id}.jpeg'
        )
    else:
        abort(404)

@pages.route('/get_lesson_thumbnail/<int:lesson_id>')
def get_lesson_thumbnail(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if lesson and lesson.thumbnail and lesson.image_mime_type:
        return send_file(
            io.BytesIO(lesson.thumbnail),
            mimetype=lesson.image_mime_type,
            as_attachment=False,
            download_name=f'lesson_{lesson_id}.jpeg'
        )
    else:
        abort(404)

@pages.route('/submit_course/<course_id>', methods=['POST'])
def submit_course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    course_title = request.form.get('course-title')
    short_course_desc = request.form.get('short-course-desc')
    full_course_desc = request.form.get('course-desc')
    course_type = request.form.get('course_type')
    skill_level = request.form.get('skill_level')
    course_thumbnail = request.files.get('thumbnail-course')

    if not short_course_desc or not full_course_desc:
        flash("Course Requires Description", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))

    if not course_title:
        flash("Course Requires Title", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))
    
    if not course_type or not skill_level:
        flash("Course Requires Course Type and Skill Level", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))

    if not course_thumbnail:
        course.thumbnail = None
        course.image_mime_type = None

    else:
        course.thumbnail = course_thumbnail.read()
        course.image_mime_type = course_thumbnail.mimetype

    course.creator = current_user.user_id 
    course.title = course_title
    course.short_desc = short_course_desc
    course.full_desc = full_course_desc
    course.course_type = course_type
    course.skill_level = skill_level

    try:
        db.session.commit()
        flash("Course Created!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for("pages.dashboard"))

@pages.route('/submit_lesson/<course_id>', methods=['POST'])
def submit_lesson(course_id):
    course = Course.query.filter_by(id=course_id).first()

    if not course:
        flash("Course Not Found", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))

    lesson_title = request.form.get('lesson-title')
    short_lesson_desc = request.form.get('short-lesson-desc')
    lesson_thumbnail = request.files.get('thumbnail-lesson')

    if not lesson_title:
        flash("Lesson Requires Title", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))
        
    if not short_lesson_desc:
        flash("Lesson Requires Description", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))

    if not lesson_thumbnail:
        image_data = None
        image_mime_type = None

    else:
        image_data = lesson_thumbnail.read()
        image_mime_type = lesson_thumbnail.mimetype

    video = request.files.get('video')
    document = request.files.get('document')
    file = request.files.get('file')

    lesson = Lesson(
            course_id=course.id,
            creator=current_user.user_id, 
            title=lesson_title, 
            short_desc=short_lesson_desc,
            thumbnail=image_data, 
            image_mime_type=image_mime_type
            )

    db.session.add(lesson)
    db.session.commit()

    flash("Lesson Added!", "success")
    return redirect(url_for('pages.create_course', course=course, course_id=course.id))

@pages.route('/edit_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    course = lesson.course

    lesson_title = request.form.get(f'lesson-title-{lesson_id}')
    short_lesson_desc = request.form.get(f'short-lesson-desc-{lesson_id}')
    lesson_thumbnail = request.files.get(f'thumbnail-lesson-{lesson_id}')

    if not lesson_title:
        flash("Lesson Requires Title", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))
        
    if not short_lesson_desc:
        flash("Lesson Requires Description", "error")
        return redirect(url_for('pages.create_course', course=course, course_id=course.id))

    if not lesson_thumbnail:
        image_data = None
        image_mime_type = None

        lesson.title = lesson_title
        lesson.short_desc = short_lesson_desc
    else:
        image_data = lesson_thumbnail.read()
        image_mime_type = lesson_thumbnail.mimetype

        lesson.title = lesson_title
        lesson.short_desc = short_lesson_desc
        lesson.thumbnail = image_data
        lesson.image_mime_type = image_mime_type

    # Add later
    video = request.files.get(f'video-{lesson_id}')
    document = request.files.get(f'document-{lesson_id}')
    file = request.files.get(f'file-{lesson_id}')

    try:
        db.session.commit()
        flash("Lesson Added!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")

    return redirect(url_for('pages.create_course', course=course, course_id=course.id))

@pages.route('/fetch4js', methods=['POST'])
@login_required
def fetch4js():
    course_id = request.json.get('course_id')  
    course = Course.query.filter_by(id=course_id).first()

    if course:
        course_data = {
            'title': course.title,
            'short_desc': course.short_desc,
            'full_desc': course.full_desc,
            'type': course.course_type,
            'level': course.skill_level
        }

        return jsonify(course_data)
    else:
        return jsonify({'error': 'Course not found'}), 404

@pages.route('/view_course/<course_id>')
@login_required
def view_course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    return render_template('view_course.html', user=current_user, course=course)

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

