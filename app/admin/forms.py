from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email,Regexp,EqualTo,ValidationError
from ..models import User


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