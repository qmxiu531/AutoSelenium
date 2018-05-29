# coding=utf-8
from selenium import webdriver
from function.base.base import Base
from function.base.comm_db import CommonDB
from function.base.excel import Excel
from function.base.automate_driver import AutomateDriver

#定义了global字典变量 g_listFun, g_dicDb, g_dicRanzhi
g_dicDb = {"host":"", "port":"", "db":"", "user":"", "password":"", "charset":""}
g_dicRanzhi = {"base_url":"", "user":"", "password":""}
g_dicFun = {"isLoad":False, "excel":""}

class BasePage(object):
    """
    Base Class for all Pages
    """
    driver = None
    base_url = None
    url = None

    def __init__(self):
        self.readConfig()       #base_page一实例化就去加载excel的配置信息

    #打开浏览器
    def open_driver(self):
        try:
            fp = webdriver.FirefoxProfile(Base.get_cur_dir(__file__) + "\\..\\firefoxPro")
            self.driver = webdriver.Firefox(fp)#打开火狐
            self.driver.maximize_window()#最大化窗口
            self.driver.implicitly_wait(10)      #隐式等待10秒
            self.keyDriver = AutomateDriver(self.driver)
            return True
        except:
            Base.printErr("打开或设置浏览器失败！")
            return False

    # 根据excel中的ranzhi--url配置地址打开
    def open_from_excel(self):
        if self.open_driver():
            self.base_url = g_dicRanzhi.get("base_url")
            self.driver.get(self.base_url)
            return True
        return False
    #关闭浏览器
    def close_driver(self):
        try:
            self.driver.close()
            return True
        except:
            Base.printErr("浏览器对象不存在！")
            return False

    #加载excel
    def readConfig(self):
        if g_dicFun.get("isLoad")==False:   #如果成立，则代表excel用例文件从来没有被加载
            excel = Excel("..\\..\\data\\RanzhiAutoCases.xlsx")
            #g_dicDb参数传参考，传进去是一个空字典，传出来则已经填充数据了
            excel.get_config_item("config", "db", g_dicDb)
            #print (g_dicDb)
            excel.get_config_item("config", "ranzhi", g_dicRanzhi)
            #print(g_dicRanzhi)
            g_dicFun["isLoad"] = True
            g_dicFun["excel"] = excel

    #打开CRM子系统
    def openCrm(self):
        try:
            self.driver.switch_to.default_content()
            self.driver.find_element_by_xpath("//li[@id='s-menu-1']//button").click()
            self.driver.switch_to.frame("iframe-1")#要点击“产品”先进入frame
            return True
        except:
            Base.printErr("打开CRM框架失败!")
            return False
    #初始化（实例化）数据库类，成为一个成员变量self.rzDB
    def init_db(self):
        host = g_dicDb.get("host")
        port = int(g_dicDb.get("port"))
        db = g_dicDb.get("db")
        user = g_dicDb.get("user")
        pwd = g_dicDb.get("password")
        charset = g_dicDb.get("charset")
        self.rzDB = CommonDB(host, port, db, user, pwd, charset)