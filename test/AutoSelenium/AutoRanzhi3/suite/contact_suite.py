from unit_test.contact_add_testcases import ContactAddTestCases1
from unit_test.contact_find_testcases import ContactFindTestCases1

class ContactSuite():
    def __init__(self, testSuite):
        self.testSuite = testSuite
    def add_tests(self):
        # 在测试套件中添加需要运行的测试用例
        self.testSuite.addTest(ContactAddTestCases1("test_contact_add_batch"))
        self.testSuite.addTest(ContactFindTestCases1("test_contact_find_batch"))
        return self.testSuite
