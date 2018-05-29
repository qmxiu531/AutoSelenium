import unittest
import time
from function.base.base import Base
from function.base.html_test_runner import HtmlTestRunner
from suite.login_suite import LoginSuite
from suite.product_suite import ProductSuite
from suite.contact_suite import ContactSuite

class RanzhiTestRunner():
    def run_tests(self):
        # 创建一个测试套件
        test_suite = unittest.TestSuite()
        # 在测试套件中添加需要运行的测试用例
        test_suite = LoginSuite(test_suite).add_tests()
        test_suite = ProductSuite(test_suite).add_tests()
        test_suite = ContactSuite(test_suite).add_tests()
        # 创建一个文本测试运行器，运行刚刚创建的测试套件
        #text_test_runner = unittest.TextTestRunner()
        #text_test_runner.run(test_suite)

        #用开源代码HtmlTestRunner运行测试套件并生成测试报告
        self.reportFile = "report\\test_result_%s.html"%time.strftime("%Y-%m-%d-%H-%M-%S")
        report = open(self.reportFile, "wb")    #用w方式打开文件，如果文件不存在则会默认创建
        html_test_runner = HtmlTestRunner(report,
                title="然之协同办公系统自动化测试结果",
                description="测试然之功能的详细自动化测试结果")

        html_test_runner.run(test_suite)
        report.close()

if __name__ == "__main__":
    test_runner = RanzhiTestRunner()
    test_runner.run_tests()
    Base.send_email("qimx@gionee.com", test_runner.reportFile)
