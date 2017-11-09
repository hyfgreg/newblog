from datetime import datetime

from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,flash
from markdown import markdown
import bleach

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique = True,index = True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash  = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default = False)
    posts = db.relationship('Post',backref = 'author', lazy = 'dynamic')

    name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    location = db.Column(db.String(64))


    def generate_confirmation_token(self,expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            flash('token错误！')
            return False
        if data.get('confirm') != self.id:
            flash('wrong id')
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_password_token(self,email,expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset_confirm':email})

    def reset_password(self,token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            flash('token错误！')
            return False
        if data.get('reset_confirm') != self.email:
            flash('邮箱错误！')
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_change_email_token(self,new_email):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'new_email':new_email,'change_email':self.id})

    def change_email(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            flash('token错误！')
            return False
        if data.get('change_email') != self.id:
            flash('token 后面有错！')
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email  = new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique = True,index = True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index = True, default = datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count = 100):
        from random import seed, randint
        import forgery_py

        seed()
        u = User.query.filter_by(role_id = 1).first()
        for i in range(count):
            p = Post(title = '第{}篇测试文章'.format(i+2),body = forgery_py.lorem_ipsum.sentences(randint(1,3)),
                     timestamp = forgery_py.date.date(True),
                     author = u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_change_body(target, value, oldvalue, intiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code',
                        'em','i','li','ol','pre','strong','ul',
                        'h1','h2','h3','p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format = 'html'),
            tags = allowed_tags, strip=True
        ))

db.event.listen(Post.body, 'set', Post.on_change_body)