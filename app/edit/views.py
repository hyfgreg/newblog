from . import edit
from flask import url_for, request, render_template, flash, redirect,session
from .forms import PostForm
from ..models import Post,User,db
from ..tools.myLogin import should_login,should_not_login, if_admin_registered,check_login


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

