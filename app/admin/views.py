from flask import url_for, request, render_template, flash, make_response, session, redirect, current_app
from . import admin
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,PasswordRestRequestForm,PasswordResetForm,EmailResetRequestForm
from ..models import User,db
from werkzeug.security import generate_password_hash, check_password_hash
from ..tools.myLogin import should_login,should_not_login, if_admin_registered,check_login
from ..email import send_email
import logging
# app = current_app._get_current_object()

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

@admin.before_app_request
def check_confirm():
    if check_login():
        if not session.get('user_help',None):
            user = User.query.filter_by(role_id =1).first()
            session['user_help'] = {'flag':user.confirmed}
        if not session['user_help']['flag'] \
            and request.endpoint[:6] != 'admin.' \
            and request.endpoint != 'static':
            return redirect(url_for('admin.unconfirmed'))


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

            session['user_help'] = {'flag': user.confirmed,'user_id':user.id}
            return resp
        flash('大兄弟，密码可不能乱来！')
    return render_template('admin/login.html', form=form)


@admin.route('/logout',methods=['GET'])
@should_login
def logout():
    session.pop('name_hash',None)
    session.pop('user_help',None)
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('name_hash','')
    flash('你已经注销了！！！')
    return resp

@admin.route('/register', methods=['GET', 'POST'])
@if_admin_registered
def register():
    form  = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data,
                    role_id = 1)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'请验证您的账号！！！',
                   template='admin/email/confirm',user = user,token = token)

        session['user_help'] = {'flag': user.confirmed,'user_id':user.id}
        flash('你已经注册，在登录后需首先验证账号！')
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html',form = form)

@admin.route('/confirm/<token>')
# @should_login
def confirm(token):
    user = User.query.filter_by(role_id = 1).first()
    if user.confirmed:
        return redirect(url_for('main.index'))
    if user.confirm(token):
        session['user_help']['flag'] = True
        flash('您的账号已经验证！')
    else:
        flash('验证地址无效或者已过期')
    return redirect(url_for('main.index'))

@admin.route('/unconfirmed')
def unconfirmed():
    if not check_login() or session['user_help']['flag']:
        return redirect(url_for('main.index'))
    flash(session['user_help']['flag'])
    return render_template('admin/unconfirmed.html')

@admin.route('/confirm')
@should_login
def resend_confirmation():
    user = User.query.filter_by(role_id = 1).first()
    token = user.generate_confirmation_token()
    send_email(user.email, '请验证您的账号！！！',
               template='admin/email/confirm', user=user, token=token)

    flash('邮件已经重新发送，请查收！')
    return redirect(url_for('main.index'))

@admin.route('/change-password',methods = ['GET','POST'])
@should_login
def change_password():
    form = ChangePasswordForm()
    user = User.query.filter_by(role_id = 1).first()
    if form.validate_on_submit():
        if user.email != form.email.data:
            flash('邮箱错误！')
            return redirect(url_for('admin.change_password'))
        elif user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.add(user)
            flash('修改密码成功')
            return redirect(url_for('main.index'))
        else:
            flash('旧密码错误！！')
            return redirect(url_for('admin.change_password'))
    return render_template('admin/change_password.html',form = form)

@admin.route('/reset',methods = ['GET','POST'])
@should_not_login
@if_admin_registered
def password_reset_request():
    form = PasswordRestRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(role_id=1).first()
        if user.email != form.email.data:
            flash('邮箱错误！')
            return redirect(url_for('admin.password_reset_request'))
        else:
            token = user.generate_reset_password_token(form.email.data)
            send_email(user.email, '请求重置密码',
                       template='admin/email/reset_password', user=user, token=token,next = request.args.get('next'))
            flash('一封邮件已经发送至您的邮箱，请查收！')
            return redirect(url_for('admin.login'))
    return render_template('admin/reset_password.html',form = form)


@admin.route('/reset/<token>',methods = ['GET','POST'])
@should_not_login
@if_admin_registered
def reset_password(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(role_id = 1).first()
        if user.reset_password(token,form.new_password.data):
            flash('重置密码成功！')
            return redirect(url_for('admin.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('admin/reset_password.html',form = form)

@admin.route('/change_email',methods = ['GET','POST'])
@should_login
@if_admin_registered
def change_email_request():
    form = EmailResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.old_email.data).first()
        if not user:
            flash('原始邮箱不正确！')
            return redirect(url_for('main.index'))
        elif user.verify_password(form.password.data):
            token = user.generate_change_email_token(form.new_email.data)
            send_email(form.new_email.data,'请验证新邮箱',
                       template='admin/email/change_email',user = user,token = token)
            flash('一封邮件已发送至您的新邮箱，请查收！')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误！')
            return redirect(url_for('main.index'))
    return render_template('admin/change_email.html',form = form)

@admin.route('/change_email/<token>')
@should_login
def change_email(token):
    user = User.query.filter_by(role_id = 1).first()
    if user.change_email(token):
        session.pop('name_hash', None)
        session.pop('user_help', None)
        resp = make_response(redirect(url_for('admin.login')))
        resp.set_cookie('name_hash', '')
        flash('修改邮箱成功！请重新登录')
        return resp
    else:
        flash('请求无效！')
    return redirect(url_for('main.index'))


