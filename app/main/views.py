from flask import render_template, session, redirect, url_for, current_app, request, flash, jsonify
from .. import db
from ..models import User, Post, BlogView, BlogViewToday, Comment, Reply
from ..email import send_email
from . import main
from .forms import CommentForm
from ..tools.myLogin import check_login


@main.route('/', methods=['GET', 'POST'])
def index():
    BlogView.add_view()
    BlogViewToday.add_today_view()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('index.html', name=session.get('username'), posts=posts, pagination=pagination)
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('index.html',name = session.get('username'),posts = posts)


@main.route('/post_<int:id>', methods=['GET', 'POST'])
def post_independent(id):
    BlogView.add_view()
    BlogViewToday.add_today_view()

    post = Post.query.filter_by(id=id).first()
    form = CommentForm(request.form, repied_id=-1)

    if form.validate_on_submit():
        comment = Comment(visitor_name=form.visitor_name.data,
                          visitor_email=form.visitor_email.data,
                          content=form.content.data,
                          post=post)
        db.session.add(comment)
        db.session.commit()
        repied_id = int(form.replied_id.data)
        if repied_id != -1:
            replied = Comment.query.get_or_404(repied_id)
            r = Reply(replier=comment, replied=replied)
            comment.comment_type = 'reply'
            comment.reply_to = replied.visitor_name
            db.session.add(r)
            db.session.add(comment)
            db.session.commit()
        flash('评论成功!')
        return redirect(url_for('.post_independent', id=post.id))

    # comments = Comment.query.filter_by(post=post).order_by(Comment.timestamp).all()
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(post=post).order_by(Comment.timestamp).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post_independent.html', post=post, comments=comments, form=form, pagination=pagination)

@main.route('/comments_ajax',methods = ['POST'])
def comments_ajax():
    try:
        id=int(request.form.get('id'))
        page = int(request.form.get('page'))
        post = Post.query.filter_by(id=id).first()
        pagination = Comment.query.filter_by(post=post).order_by(Comment.timestamp).paginate(
            page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
            error_out=False)
        comments = pagination.items
        data = []
        for c in comments:
            sc = {
                'visitor_name':c.visitor_name,
                'content':c.content,
                'timestamp':c.timestamp,
                'reply_to':c.reply_to,
                'comment_type':c.comment_type,
                'id':id
            }
            data.append(sc)
        return jsonify({'msg':'ok','data':data})
    except Exception as e:
        return jsonify({'msg':e.args})

@main.route('/about_me')
def about_me():
    BlogView.add_view()
    BlogViewToday.add_today_view()
    user = User.query.filter_by(role_id=1).first()

    return render_template('about_me.html', user=user)
