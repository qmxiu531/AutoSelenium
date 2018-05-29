# -*- coding: utf-8 -*-
"""
1. 引入 unittest 模组
2. 继承 untitest.TestCase 类
3. 测试用例的方法必须以 test 开头
4.每一个测试用例执行前会先执行setUp，执行完后会执行tearDown
5.TestCase类中有一系列的断言语句，帮助判断执行结果
6.一个测试用例失败后不会影响其他测试用例的执行
"""

import unittest
from function.page.login_page import RanzhiLogin
from function.base.base import *

class LoginTestCases1(unittest.TestCase):
    def setUp(self):
        print("-- testcase start --")
        self.rzLogin = RanzhiLogin()
        self.succ = "PASS--"

    def tearDown(self):
        print("-- testcase finished --")
        pass

    def test_log_in_01(self):
        print("-- testcase_01 正确的用户名密码 --")
        self.rzLogin.log_in("admin", "111111")
        #调用模块化的验证函数以此判断登录是否成功
        rc = self.rzLogin.v_login(True, "admin", "")
        self.assertIn(self.succ, rc)
    def test_log_in_02(self):
        print("-- testcase_02 错误的用户名密码 --")
        self.rzLogin.log_in("abcdef", "222222")
        rc = self.rzLogin.v_login(False, "", \
                    "登录失败，请检查您的成员名或密码是否填写正确。")
        self.assertIn(self.succ, rc)

    def test_log_in_03(self):
        print("-- testcase_03 空的用户名或密码 --")
        self.rzLogin.log_in("cdefab", "")
        rc = self.rzLogin.v_login(False, "",
                                  "登录失败，用户名或密码不能为空。")
        self.assertIn(self.succ, rc)

    def test_log_in_04(self):
        print("-- testcase_04 正确的用户名密码 --")
        self.rzLogin.log_in("admin", "111111")
        rc = self.rzLogin.v_login(True, "admin", "")
        self.assertIn(self.succ, rc)

#if __name__ == "__main__":
#    unittest.main()
