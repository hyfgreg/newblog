from ..models import db,Post
from flask import current_app

def recent_posts():
    recent_posts = Post.query.filter_by(open_flag=1).order_by(Post.timestamp.desc()).limit(current_app.config['RECENT_POSTS'])
    return recent_posts