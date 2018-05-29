# coding=utf-8

from selenium import webdriver
from function.base.base import Base
from function.base.base_page import BasePage
from time import sleep

#封装然之登录页面功能类
class RanzhiLogin(BasePage):
    #然之页面的登录操作
    #self.url:然之的网址
    #username：登录然之的用户名
    #password：登录然之的密码
    def log_in(self, username, password):
        if self.open_from_excel()==False:      #根据excel中的url打开浏览器
            return None
        sleep(1)                            #等待1秒（可选）
        try:
            self.driver.find_element_by_id("account").send_keys(username)#定位到用户名字段并输入用户名
            self.driver.find_element_by_id("password").send_keys(password)#定位到密码字段并输入密码
            self.driver.find_element_by_id("submit").click()        #点击登录按钮
            sleep(1)
            return self.driver

        except:
            Base.printErr("ERR--log_in方法中登录然之操作失败.")
            return None
    #这个函数负责登录后验证登录结果是否满足期望的结果
    #status:登录的期望状态是：True:成功；False：失败
    #expectUser:登录成功的期望用户名
    #expectInfo：登录失败的期望提示信息
    def v_login(self, status, expectUser, expectInfo):
        rc = ""
        try:
            if status:  #如果登录的期望结果是成功的
                #从登陆成功的界面上获取用户名
                userLogin = self.driver.find_element_by_css_selector\
                    ("ul[class='nav navbar-nav']>li>a").text
                #如果从界面上获取的用户名和期望的用户名相等
                if userLogin == expectUser:
                    rc = "PASS--登录成功：" + expectUser   #返回验证成功信息
                else:
                    #返回验证失败信息
                    rc = "FAIL--登录错误，期望用户为‘%s’,实际用户为‘%s’"\
                         %(expectUser,userLogin)
            else:       #如果登录的期望结果是失败的
                #获取登录失败提示框中的提示信息
                errBoxMsg = self.driver.find_element_by_class_name("bootbox-body").text
                #如果界面上获取的错误提示信息和期望的错误提示信息相等
                if errBoxMsg == expectInfo:
                    rc = "PASS--预期的登录错误提示信息验证成功！"   #返回验证成功信息
                else:   #否则不相等
                    #返回验证失败信息
                    rc = "FAIL--登录验证失败，期望错误信息为‘%s’，实际错误信息为‘%s’" \
                          %(expectInfo,errBoxMsg)
        except:
            Base.printErr("ERR--v_login方法验证登陆时失败")
            return rc

            #raise rc
        self.close_driver()       #关闭浏览器
        return rc                 #将验证成功、失败、错误等信息返回给调用者

#下面写几个测试用例来调用上述函数做测试
if __name__=="__main__":
    rzLogin = RanzhiLogin()   #实例化上面的然之登录类
    print("-- testcase_01 正确的用户名密码 --")         #打印提示当前用例名称
    rzLogin.log_in("admin", "111111")          #调用类方法用正确的用户名admin密码111111登录然之
    x = rzLogin.v_login(True, "admin", "")
    print(x)  #调用类方法验证登录后的结果检查点

    print("-- testcase_02 错误的用户名密码 --")
    rzLogin.log_in("abcd", "222222")
    print(rzLogin.v_login(False, "", "登录失败，请检查您的成员名或密码是否填写正确。"))

    print("-- testcase_03 空的用户名/密码 --")
    rzLogin.log_in("cdef", "")
    print(rzLogin.v_login(False, "", "登录失败, 用户名或密码不能为空"))