from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file, abort
from flask_login import login_required, current_user
from .models import db, User 

pages = Blueprint("pages", __name__)

@pages.route('/')
@pages.route('/home')
def home():
    return render_template('index.html', user=current_user)

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

