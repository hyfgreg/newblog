from ..models import db,Post

def recent_posts():
    recent_posts = Post.query.order_by(Post.timestamp.desc()).limit(3)
    return recent_posts