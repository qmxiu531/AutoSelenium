from unit_test.login_testcases_01 import LoginTestCases1
from unit_test.login_testcases_02 import LoginTestCases2

class LoginSuite():
    def __init__(self, testSuite):
        self.testSuite = testSuite
    def add_tests(self):
        # 在测试套件中添加需要运行的测试用例
        # 一个测试套件中可以添加多个测试用例
        self.testSuite.addTest(LoginTestCases1("test_log_in_01"))
        self.testSuite.addTest(LoginTestCases1("test_log_in_02"))
        self.testSuite.addTest(LoginTestCases1("test_log_in_03"))
        self.testSuite.addTest(LoginTestCases1("test_log_in_04"))
        self.testSuite.addTest(LoginTestCases2("test_log_in_batch"))
        return self.testSuite
