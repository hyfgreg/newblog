from flask import request,session,redirect,url_for,current_app,flash
from functools import wraps
from ..models import User


def check_login():
    name_hash = request.cookies.get('name_hash', None)
    # print(session['name_hash'])
    name_hash_sess = session.get('name_hash', None)
    if name_hash and name_hash_sess and name_hash == name_hash_sess:
        return True
    return False

def should_login(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        # name_hash = request.cookies.get('name_hash','None')
        if not check_login():
            flash('请登录！！！')
            return redirect(url_for('main.index'))
        return func(*args,**kwargs)
    return wrap

def should_not_login(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        name_hash = request.cookies.get('name_hash',None)
        if name_hash and name_hash == session.get('name_hash'):
            return  redirect(url_for('main.index'))
        return func(*args,**kwargs)
    return wrap


def if_admin_registered(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        user = User.query.filter_by(role_id = 1).first()
        if user and request.endpoint[:] == 'admin.register':
            return redirect(url_for('admin.login'))
        elif not user and request.endpoint[:] == 'admin.login':
            return redirect(url_for('admin.register'))
        return func(*args,**kwargs)
    return wrap

