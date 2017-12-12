#!/usr/bin/env python
import os

import datetime
from app import create_app, db
from app.models import User, Role, Post, BlogView, BlogViewToday, Comment, Reply
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.tools.myLogin import check_login
from app.tools.utils import recent_posts

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

# @app.context_processor
# def get_check_login():
#     return dict(check_login = check_login)

app.jinja_env.globals['datetime'] = datetime
app.jinja_env.globals['check_login'] = check_login
app.jinja_env.globals['recent_posts'] = recent_posts
app.jinja_env.globals['BlogView'] = BlogView
app.jinja_env.globals['BlogViewToday'] = BlogViewToday


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, BlogView=BlogView, BlogViewToday=BlogViewToday,
                Comment=Comment, Reply=Reply)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
