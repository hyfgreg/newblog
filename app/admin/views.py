from flask import url_for,request, render_template, flash, make_response, session, redirect
from . import admin
from .forms import LoginForm
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..tools.myLogin import should_not_login, if_admin_registered
import logging

# 去掉链接末尾的/，这是个大坑，比如/admin/register可以访问，但是/admin/register/就不可以访问了
# 但是奇怪的是，/admin/register这样子，flask会自动处理成/admin/register/
# 但是直接在末尾加一个/就不能访问了，实在是太奇怪了！！！
@admin.before_app_request
def clear_trailing():
    rp = request.path
    # print(rp)
    if rp != '/' and rp != '/admin/' and rp.endswith('/'):
        rp = rp[:-1]
        if len(request.query_string) > 0:
            rp = rp + '?' + request.query_string
        return redirect(rp)



@admin.route('/', methods=['GET', 'post'])
@should_not_login
@if_admin_registered
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            name_hash = generate_password_hash(user.username)
            session['name_hash'] = name_hash
            session['username'] = user.username
            resp = make_response(redirect(url_for('main.index')))
            resp.set_cookie('name_hash', name_hash)
            return resp
        flash('大兄弟，密码可不能乱来！')
    return render_template('admin/login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
@if_admin_registered
def register():
    return '<h1>这是一个注册界面</h1>'
