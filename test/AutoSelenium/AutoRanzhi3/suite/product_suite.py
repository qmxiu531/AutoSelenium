from unit_test.product_add_testcases_01 import ProductAddTestCases1

class ProductSuite():
    def __init__(self, testSuite):
        self.testSuite = testSuite
    def add_tests(self):
        # 在测试套件中添加需要运行的测试用例
        self.testSuite.addTest(ProductAddTestCases1("test_product_add_batch"))
        return self.testSuite
