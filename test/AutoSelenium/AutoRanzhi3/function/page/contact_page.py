# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from function.base.base_page import *
from function.page.login_page import RanzhiLogin
import unittest
from time import sleep

#这个类封装了产品的功能
class RanzhiContact(RanzhiLogin):
    #构造函数
    def __init__(self):
        super(RanzhiContact, self).__init__()
        self.init_db()
    #析造函数
    def __del__(self):
        pass

    def inputContact(self, case):
        try:
            self.keyDriver.type("i,realname", case[1])
            if case[2]:
                self.keyDriver.click("i,maker")
            if case[4]:
                self.keyDriver.click("i,newCustomer")
                self.keyDriver.type("i,name", case[3])
            elif case[3]:
                self.keyDriver.type("s,div[class='chosen-search']>input", case[3] + Keys.RETURN)
            sleep(1)
            if case[5]=="男":
                self.keyDriver.click("i,gender1")
            elif case[5]=="女":
                self.keyDriver.click("i,gender2")
            self.keyDriver.type_d("i,dept", case[6])
            self.keyDriver.type_d("i,title", case[7])
            self.keyDriver.type_d("i,join", case[8])
            self.keyDriver.type_d("i,email", case[9])
            self.keyDriver.type_d("i,mobile", case[10])
            self.keyDriver.type_d("i,phone", case[11])
            self.keyDriver.type_d("i,fax", case[12])
            self.keyDriver.type_d("i,qq", case[13])
            self.keyDriver.select_by_visible_text_d("i,type", case[14])
            self.keyDriver.select_by_visible_text_d("i,size", case[15])
            self.keyDriver.select_by_visible_text_d("i,status", case[16])
            self.keyDriver.select_by_visible_text_d("i,level", case[17])
            self.keyDriver.type_d("i,createdDate",case[18])
            self.keyDriver.type_d("i,desc",case[19])
        except:
            Base.printErr("输入联系人信息失败!")

    #是否保存
    def isSave(self, bSave):
        if bSave:
            self.keyDriver.click("i,submit")
        else:
            self.keyDriver.click("s,input[class='btn btn-default']")    #取消按钮

    #操作产品的添加
    def ranzhi_contact_add(self, case):
        try:
            self.openCrm()
            self.keyDriver.click("l,联系人")
            #添加一个新联系人
            self.keyDriver.click("l,添加联系人")
            self.inputContact(case)
            self.isSave(True)
            sleep(2)
            try:
                self.keyDriver.click("i,continueSubmit")
            except:
                pass
        except:
            Base.printErr("添加联系人失败!")

    def ranzhi_contact_add_v(self, case):
        try:
            #界面验证
            if case[20]:
                sleep(2)
                #验证联系人列表是否保存成功
                contactName = self.keyDriver.get_text("x,//table[@id='contactList']/tbody/tr[1]/td[2]")
                customerName = self.keyDriver.get_text("x,//table[@id='contactList']/tbody/tr[1]/td[3]")
                unittest.TestCase().assertEqual(case[1], contactName)
                unittest.TestCase().assertEqual(case[3], customerName)
            else:
                actual = self.keyDriver.get_text("s,table[class='table table-form']")   #得到的是整个Form中的文字
                expList = case[21].split(";")   #真实姓名不能为空;所属客户不能为空
                for li in expList:
                    unittest.TestCase().assertIn(li, actual)
            #数据库验证
            dbrc = self.rzDB.execSql(case[23], True)
            if dbrc[0] == False:
                return "ERR--数据库操作失败，信息：%s"%dbrc[1]
            else:
                if dbrc[1] != 1:
                    return "FAIL--数据库验证返回False!"
        except:
            return Base.printErr("ERR--验证然之产品添加时失败！", False)
        return "PASS--联系人添加/验证成功：%s"%case[1]

#开始写调试代码，调试上面的联系人类
if __name__=='__main__':
    rzContact = RanzhiContact()
    ex = g_dicFun.get("excel")
    #用例一：正确的联系人添加，用例执行成功
    case = ["正确的联系人","张三",True,"51testing",
            True,"男","就业部","员工","2017/1/1",
            "zs@51testing.com","13923567890","0755-23456789",
            "0755-54345678","45678900@qq.com","股份企业","大型(100人以上)",
            "意向","A(有明显的业务需求，预计一个月内成交)","#d#","资深就业老师，南开大学研究生毕业",
            True,"","delete from crm_contact where realname='张三'",
            "select count(*)=1 from crm_contact where realname='张三'","",""]
    rzContact.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
    s =  ex.str_parse_func(case[22])
    rzContact.rzDB.execSql(s)
    rzContact.ranzhi_contact_add(case)
    print(rzContact.ranzhi_contact_add_v(case))
    rzContact.close_driver()


    rzContact = RanzhiContact()
    ex = g_dicFun.get("excel")
    #用例二：错误的联系人添加，用例执行成功
    case = ["正确的联系人","",True,"",
            True,"男","就业部","员工","2017/1/1",
            "zs@51testing.com","13923567890","0755-23456789",
            "0755-54345678","45678900@qq.com","股份企业","大型(100人以上)",
            "意向","A(有明显的业务需求，预计一个月内成交)","#d#","资深就业老师，南开大学研究生毕业",
            False,"真实姓名不能为空;所属客户不能为空","delete from crm_contact where realname=''",
            "select count(*)=0 from crm_contact where realname=''","",""]
    rzContact.log_in(g_dicRanzhi.get("user"), g_dicRanzhi.get("password"))
    s =  ex.str_parse_func(case[22])
    rzContact.rzDB.execSql(s)
    rzContact.ranzhi_contact_add(case)
    print(rzContact.ranzhi_contact_add_v(case))
    rzContact.close_driver()
