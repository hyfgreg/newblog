from flask import render_template, session, redirect, url_for, current_app,request
from .. import db
from ..models import User,Post
from ..email import send_email
from . import main
from .forms import NameForm
from ..tools.myLogin import check_login


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page',1,type = int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('index.html',name = session.get('username'),posts = posts,pagination = pagination)
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('index.html',name = session.get('username'),posts = posts)