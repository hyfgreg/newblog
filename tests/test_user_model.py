import unittest
from ..app.models import User

class UserModelTestCase(unittest.TestCase):
    #测试密码散列值可以生成
    def test_password_setter(self):
        u = User(password='123')
        self.assertTrue(u.password_hash is not None)

    #测试散列值不可读属性
    def test_no_password_getter(self):
        u = User(password='123')
        with self.assertRaises(AttributeError):
            u.password

    #测试密码可以正确认证
    def test_password_verification(self):
        u = User(password='123')
        self.assertTrue(u.verify_password('123'))
        self.assertFalse(u.verify_password('321'))

    #测试密码相同散列值也是不同的
    def test_password_salts_are_random(self):
        u = User(password='123')
        u2 = User(password='123')
        self.assertTrue(u.password_hash != u2.password_hash)
