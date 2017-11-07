from flask import render_template, session, redirect, url_for, current_app,request
from .. import db
from ..models import User,Post
from ..email import send_email
from . import main
from .forms import NameForm
from ..tools.myLogin import check_login


@main.route('/', methods=['GET', 'POST'])
def index():
    # name_hash = request.cookies.get('name_hash',None)
    # # print(session['name_hash'])
    # name_hash_sess = session.get('name_hash',None)
    # if name_hash and name_hash_sess and name_hash == name_hash_sess:
    # if check_login():
    #     return render_template('index.html',
    #                        name =session.get('username'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',name = session.get('username'),posts = posts)