# -*- coding: gbk -*-
import unittest         #引入单元测试框架
from function.page.login_page import *    #引入自定义的公用操作包
from function.base.base import *
from function.base.base_page import *

class LoginTestCases2(unittest.TestCase):
    def setUp(self):                    #初始化测试用例，前置条件
        print("-- testcase start --")
        #实例化RanzhiLogin类，并传入URL
        self.rzLogin = RanzhiLogin()
        #定义一个成员变量，作为验证是否成功的标签
        self.succ = "PASS--"

    def tearDown(self): #测试收尾工作
        print("-- testcase finished --")

    def test_log_in_batch(self):
        #这里采用数据驱动的方法
        #数据驱动：将测试数据和业务逻辑剥离，这里将登录用户密码单独定义到一个csv文件中，
        # 测试执行员只需要维护好该数据即可
        #业务逻辑则由自动化编程人员在测试程序中实现，该程序自动调用独立测试数据文件完成测试
        #首先打开测试用例文件
        ex = g_dicFun.get("excel")
        cases = ex.get_page_data("login")
        x = 0   #定义一个计数器，用于识别用例文件中的第一行
        fNum = 0            #失败的用例数
        cNum = 0            #总用例数
        for case in cases:    #循环二维数组，每循环一次取出一行数据（一维数组）
            if x == 0:                          #如果是第一行（第一次循环）
                x += 1
                continue

            print("-- testcase：%s --"%case[0])   #打印测试用例名称user[0]到输出屏幕
            self.rzLogin.log_in(case[1], case[2])   #调用公用函数执行登录然之
            if case[4] == "":                   #如果第五个数据是空的，那么就用第二个
                case[4]=case[1]
            rc = self.rzLogin.v_login(case[3], case[4], case[4])#调用公用函数执行登录后验证
            try:
                res = "Pass"                #首先认为本用例是成功的
                msg = ""
                self.assertIn(self.succ, rc) #从验证的结果串中断言一下是否成功（包含'PASS--'则为成功）
            except:          #如果跳到了except子句则表示有用例验证失败
                res = "Failed"              #本用例失败了
                msg = rc                #记录失败的错误信息
                Base.printErr()                   #把失败的信息打印到屏幕
                fNum = fNum + 1
            #将结果写入到user_login_res.csv中
            cNum = cNum + 1
            ex.write_by_index(x, 5, "login", res)
            ex.write_by_index(x, 6, "login", msg)
            x += 1
            ex.save_excel()
        #断言如果allMsg中有内容则为本用例集中存在失败的用例，抛出错误信息
        self.assertEqual(fNum, 0, "总用例数:%d,失败用例数:%d."%(cNum, fNum))