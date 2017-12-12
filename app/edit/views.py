from . import edit
from flask import url_for, request, render_template, flash, redirect, session, current_app, jsonify
from .forms import PostForm
from ..models import Post,User,db
from ..tools.myLogin import should_login,should_not_login, if_admin_registered,check_login

# 这个是用来处理地址最后的'/'
@edit.before_app_request
def clear_trailing():
    rp = request.path
    # print(rp)
    if rp != '/' and rp != '/admin/' and rp.endswith('/'):
        rp = rp[:-1]
        if len(request.query_string) > 0:
            rp = rp + '?' + request.query_string
        return redirect(rp)

@edit.before_app_request
def check_confirm():
    if check_login():
        if not session.get('user_help',None):
            user = User.query.filter_by(role_id =1).first()
            session['user_help'] = {'flag':user.confirmed}
        if not session['user_help']['flag'] \
            and request.endpoint[:6] != 'admin.' \
            and request.endpoint != 'static':
            return redirect(url_for('admin.unconfirmed'))

@edit.route('/newpost',methods = ['GET','POST'])
@should_login
@if_admin_registered
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(role_id = 1).first()

        post = Post(title = form.title.data,
                    body = form.body.data,
                    author_id = session['user_help'].get('user_id'))
        db.session.add(post)
        flash('发表文章成功')
        return redirect(url_for('main.index'))
    return render_template('edit/newpost.html',form = form)

@edit.route('/posts_management')
@should_login
@if_admin_registered
def posts_management():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('edit/posts_management.html', name=session.get('username'), posts=posts, pagination=pagination)

@edit.route('/edit_post/<int:id>',methods = ['GET','POST'])
@should_login
@if_admin_registered
def edit_post(id):
    post = Post.query.filter_by(id = id).first()
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash('更新文章成功')
        return redirect(url_for('main.index'))
    ###一定要放到if form.validate_on_submit后面！！！否则无法更新文章
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit/newpost.html', form=form)

@edit.route('/open_hide_post/<int:id>',methods = ['GET','POST'])
@should_login
@if_admin_registered
def open_hide_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.open_flag:
        post.open_flag = False
        flag = '隐藏'
    else:
        post.open_flag = True
        flag = '公开'
    db.session.add(post)
    flash('更新文章《{}》状态为<{}>'.format(post.title,flag))
    return redirect(url_for('edit.posts_management'))

@edit.route('/open_hide_post_ajax',methods = ['GET','POST'])
@should_login
@if_admin_registered
def open_hide_post_ajax():
    try:
        id=int(request.form.get('id'))
        post = Post.query.filter_by(id=id).first()
        if post.open_flag:
            post.open_flag = False
            flag = '隐藏'
        else:
            post.open_flag = True
            flag = '公开'
        db.session.add(post)
        db.session.commit()
        return jsonify({'result':'ok'})
    except Exception as e:
        return jsonify({'result':e.args})
