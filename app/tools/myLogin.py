from flask import request,session,redirect,url_for,current_app,flash
from functools import wraps
from ..models import User

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
        if not user:
            return redirect(url_for('admin.register'))
        elif user.username == 'hyfgreg' and request.endpoint[:] == 'admin.register':
            # flash(request.endpoint[:])
            return redirect(url_for('admin.login'))
        return func(*args,**kwargs)
    return wrap

