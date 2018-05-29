# -*- coding: gbk -*-
import csv              #引入csv包
import unittest         #引入单元测试框架

from function.page.product_page import *     #引入自定义的公用操作包
from function.base.comm_db import CommonDB   #引入自定义的然之数据库操作类


class ProductAddTestCases1(unittest.TestCase):
    def setUp(self):#初始化测试用例，前置条件
        print("-- testcases start --")
        self.rzProduct = RanzhiProduct()
        self.m_db = self.rzProduct.rzDB
        self.succ = "PASS--"

    def tearDown(self): #测试收尾工作
        print("-- testcases finished --")


    def test_product_add_batch(self):
        #这里采用数据驱动的方法
        #数据驱动：将测试数据和业务逻辑剥离，这里将登录用户密码单独定义到一个csv文件中，
        # 测试执行员只需要维护好该数据即可
        #业务逻辑则由自动化编程人员在测试程序中实现，该程序自动调用独立测试数据文件完成测试
        ex = g_dicFun.get("excel")
        cases = ex.get_page_data("productAdd")
        x = 0
        nCount = 0  #计算执行的用例总数
        nFail = 0   #计算失败用例数
        for case in cases:
            if x == 0:                          #如果是第一行（第一次循环）
                x += 1
                continue
            print("-- testcase：%s --"%case[0])                 #开始一份测试用例的执行
            try:
                self.rzProduct.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
                case[7] =  ex.str_parse_func(case[7])   #前置SQL
                case[8] = ex.str_parse_func(case[8])    #验证SQL
                dbrc = self.m_db.execSql(case[7])
                if dbrc[0] == False:   #执行SQL语句出错的处理
                   print(dbrc[1])
                self.rzProduct.ranzhi_product_add(case)      #调用公用函数执行产品添加
                rc = self.rzProduct.ranzhi_product_add_v(case)         #调用公用函数执行登录后验证
                res = "Pass"                #首先认为本用例是成功的
                msg = ""
                self.assertIn(self.succ, rc) #从验证的结果串中断言一下是否成功（包含'PASS--'则为成功）
            except:          #如果跳到了except子句则表示有用例验证失败
                res = "Failed"              #本用例失败了
                msg = Base.printErr()
                nFail += 1
                #截图
                #self.rzProduct.getDriver().save_screenshot("c:\\screenshot.jpg")
            nCount += 1
            #将结果写入到结果Excel中
            ex.write_by_index(x, 9, "productAdd", res)
            ex.write_by_index(x, 10, "productAdd", msg)
            x += 1
            self.rzProduct.close_driver()
        #断言失败用例数是否等于0
        ex.save_excel()
        self.assertEqual(nFail, 0, "共执行用例数:%d;其中失败用例数:%d"%(nCount, nFail))
