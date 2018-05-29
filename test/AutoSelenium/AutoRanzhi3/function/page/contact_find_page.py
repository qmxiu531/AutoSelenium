# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from function.base.base_page import *
from function.page.login_page import RanzhiLogin
import unittest
from time import sleep

#这个类封装了产品的功能
class RanzhiContactFind(RanzhiLogin):
    #构造函数
    def __init__(self):
        super(RanzhiContactFind, self).__init__()
        self.init_db()
    #析造函数
    def __del__(self):
        pass

    #输入查询条件
    def inputCond(self, case):
        try:
            strCondtion = case[1]

            listTeam = strCondtion.split("$$$")
            if len(listTeam)>=1:
                listItem = listTeam[0].split(",")
                i = 0
                j = 1
                while i<len(listItem):
                    if i > 0:
                        self.keyDriver.select_by_visible_text("i,andOr%d"%(j), listItem[i])
                        i += 1
                    self.keyDriver.select_by_visible_text("n,field%d"%(j), listItem[i])
                    self.keyDriver.select_by_visible_text("n,operator%d"%(j), listItem[i+1])
                    if self.keyDriver.get_display("n,value%d"%(j)):
                        self.keyDriver.type("n,value%d"%(j), listItem[i+2])
                    else:
                        self.keyDriver.click("x,//td[@id='valueBox%d']//a"%j)
                        self.keyDriver.type("x,//td[@id='valueBox%d']//input"%j,  listItem[i+2] + Keys.RETURN)
                    i += 3
                    j += 1
            if len(listTeam)==2:
                listItem = listTeam[1].split(",")
                i = 0
                j = 4
                self.keyDriver.select_by_visible_text("n,groupAndOr", listItem[0])  #组并且/或者
                listItem.pop(0)
                while i<len(listItem):
                    if i > 0:
                        self.keyDriver.select_by_visible_text("i,andOr%d"%(j), listItem[i])
                        i += 1
                    self.keyDriver.select_by_visible_text("n,field%d"%(j), listItem[i])
                    self.keyDriver.select_by_visible_text("n,operator%d"%(j), listItem[i+1])
                    if self.keyDriver.get_display("n,value%d"%(j)):
                        self.keyDriver.type("n,value%d"%(j), listItem[i+2])
                    else:
                        self.keyDriver.click("x,//td[@id='valueBox%d']//a"%j)
                        self.keyDriver.type("x,//td[@id='valueBox%d']//input"%j,  listItem[i+2] + Keys.RETURN)
                    i += 3
                    j += 1
        except:
            Base.printErr("输入查询条件失败，可能是数据格式错误!")

    #操作联系人的查询
    def ranzhi_contact_find(self, case):
        try:
            self.openCrm()
            self.keyDriver.click("l,联系人")
            sleep(1)
            #点击搜索
            self.keyDriver.click("s,#bysearchTab>a")
            sleep(1)
            self.keyDriver.click("i,searchmore")
            sleep(1)
            self.inputCond(case)
            self.keyDriver.click("i,submit")
            sleep(2)
        except:
            Base.printErr("查询联系人失败!")

    #验证查询结果的正确性
    def ranzhi_contact_find_v(self, case):
        try:
            ut = unittest.TestCase()
            #读取查询结果行数
            rows = self.keyDriver.get_elements("x,//table[@id='contactList']/tbody/tr")
            realNum = len(rows)
            expNum= int(case[2])
            ut.assertEqual(realNum, expNum,
                            "期望的结果行数：%d；实际结果行数：%d"%(expNum, realNum))
            verKeys = case[3].split(";")
            i = 1
            for row in rows:
                rowTxt = row.text
                for key in verKeys:
                    ut.assertIn(key, rowTxt,
                                "关键字'%s'在第 %d 行中不存在，验证失败"%(key, i))
                i += 1
        except:
            return Base.printErr("联系人查询验证失败！", False)
        return "PASS--联系人查询验证成功：%s"%case[0]

#开始写调试代码，调试上面的产品类
if __name__=='__main__':
    rzContact = RanzhiContactFind()
    ex = g_dicFun.get("excel")
    #用例一：正确的产品添加，用例执行成功
    case = ["多条件-分组姓名及客户",
            "真实姓名,=,里斯,或者,所属客户,包含,深圳市电视台,或者,电话,包含,0755-$$$"
            "并且,手机,=,13911112222,并且,电话,包含,0755-89009999,或者,邮箱,=,351867355@qq.com",
            1,
            "里斯",
            "$sql.insContact()"]

    s =  ex.str_parse_func(case[4])
    rzContact.rzDB.execSql(s)
    rzContact.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
    rzContact.ranzhi_contact_find(case)
    print(rzContact.ranzhi_contact_find_v(case))
    rzContact.close_driver()