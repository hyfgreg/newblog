from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Email, Length, DataRequired,Required


# class NameForm(FlaskForm):
#     name = StringField('What is your name?', validators=[Required()])
#     submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    visitor_name = StringField('请输入你的名字', validators=[DataRequired(message=u'名字不能为空！')])
    visitor_email = StringField('请输入你的邮箱',
                                validators=[Length(1, 64), Email(message=u'请输入有效的邮箱地址，比如：username@domain.com'),
                                            DataRequired(message=u'请输入正确邮箱！')])
    content = TextAreaField('尽情发挥！', validators=[DataRequired(message='内容不能为空！')])
    submit = SubmitField('提交')
