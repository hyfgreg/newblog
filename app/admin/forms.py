from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import Required, Length, Email,Regexp,EqualTo,ValidationError
from ..models import User


class TestForm(FlaskForm):
    email = StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    submit = SubmitField('登录')

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(),Length(1,64),Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登录')

    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    username = StringField('用户名',validators=[Required(),Length(1,64),
                                             Regexp('^[A-Za-z0-9_.]*$',0,
                                                    '用户名仅能含有字母、数字、点、下划线！！！')])
    password = PasswordField('密码',validators=[Required(),EqualTo('password2',message='请输入相同密码！！！')])
    password2 = PasswordField('确认密码',validators=[Required()])

    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('邮箱已存在！！！')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已存在！！！')

class ChangePasswordForm(FlaskForm):
    email = StringField('邮箱',validators=[Required(),Length(1,64),Email()])
    old_password = PasswordField('旧密码',validators=[Required(),])
    new_password = PasswordField('新密码',validators=[Required(),EqualTo('new_password2',message='请输入相同密码！！！')])
    new_password2 = PasswordField('确认新密码', validators=[Required(), ])
    submit = SubmitField('提交')

class PasswordRestRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('提交')


class PasswordResetForm(FlaskForm):
    new_password = PasswordField('新密码', validators=[Required(), EqualTo('new_password2', message='请输入相同密码！！！')])
    new_password2 = PasswordField('确认新密码', validators=[Required(), ])
    submit = SubmitField('提交')

class EmailResetRequestForm(FlaskForm):
    old_email = StringField('旧邮箱',validators=[Required(),Length(1,64),Email()])
    password  = PasswordField('密码',validators=[Required(),])
    new_email = StringField('新邮箱',validators=[Required(),Length(1,64),Email(),EqualTo('new_email2', message='请输入相同邮箱！！！')])
    new_email2 = StringField('确认新邮箱',validators=[Required(),Length(1,64),Email()])
    submit = SubmitField('提交')

class PostForm(FlaskForm):
    title = StringField('标题',validators=[Required(),Length(1,512)])
    body = TextAreaField('写点什么吧~',validators=[Required()])
    submit = SubmitField('提交')