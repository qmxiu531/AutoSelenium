# -*- coding: gbk -*-
import unittest         #引入单元测试框架

from function.page.contact_find_page import *     #引入自定义的公用操作包

class ContactFindTestCases1(unittest.TestCase):
    def setUp(self):#初始化测试用例，前置条件
        print("-- testcases start --")
        self.rzContact = RanzhiContactFind()
        self.m_db = self.rzContact.rzDB
        self.succ = "PASS--"

    def tearDown(self): #测试收尾工作
        print("-- testcases finished --")


    def test_contact_find_batch(self):
        #这里采用数据驱动的方法
        ex = g_dicFun.get("excel")
        cases = ex.get_page_data("contactFind")
        x = 0
        nCount = 0  #计算执行的用例总数
        nFail = 0   #计算失败用例数
        for case in cases:
            if x == 0:                              #如果是第一行（第一次循环）
                x += 1
                continue
            print("-- testcase：%s --"%case[0])   #开始一份测试用例的执行
            try:
                self.rzContact.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
                case[4] =  ex.str_parse_func(case[4])
                case[5] = ex.str_parse_func(case[5])
                if case[4] != "":
                    dbrc = self.m_db.execSql(case[4])
                if dbrc[0] == False:   #执行SQL语句出错的处理
                   print(dbrc[1])
                self.rzContact.ranzhi_contact_find(case)      #调用公用函数执行产品添加
                rc = self.rzContact.ranzhi_contact_find_v(case)         #调用公用函数执行登录后验证
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
            ex.write_by_index(x, 6, "contactFind", res)
            ex.write_by_index(x, 7, "contactFind", msg)
            x += 1
            self.rzContact.close_driver()
        #断言失败用例数是否等于0
        ex.save_excel()
        self.assertEqual(nFail, 0, "共执行用例数:%d;其中失败用例数:%d"%(nCount, nFail))
