from flask import render_template, session, redirect, url_for, current_app,request
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    name_hash = request.cookies.get('name_hash',None)
    if name_hash and name_hash == session['name_hash']:
        return render_template('index.html',
                           name =session.get('username'))
    return render_template('index.html')