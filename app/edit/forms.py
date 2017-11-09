from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    title = StringField('标题',validators=[Required(),Length(1,512)])
    body = PageDownField('写点什么吧~',validators=[Required()])
    submit = SubmitField('提交')