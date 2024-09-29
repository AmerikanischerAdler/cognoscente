from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, send_file, abort
from flask_login import login_required, current_user
from .models import db, User 

pages = Blueprint("pages", __name__)

@pages.route('/')
@pages.route('/home')
def home():
    return render_template('index.html', user=current_user)

