# -*- coding: utf-8 -*-
import xlrd, xlwt
from xlutils.copy import copy
import time
from function.base.base import Base

class Excel(object):
    def __init__(self, file):
        #一个软件只有一个工作路径，所以当有可能从不同的入口执行时，需要获取当前的绝对路径，再去查找相对路径
        self.file = Base.get_cur_dir(__file__)  + "\\" + file#永远是基于excel.py所在路径
        self.targetName = self.file.replace(".xlsx", (time.strftime("%Y-%m-%d-%H-%M-%S") + ".xlsx"))
        self.data = None
    #打开excel文件
    def open_excel(self):
        try:
            if not self.data:
                self.data = xlrd.open_workbook(self.file)
                self.target = copy(self.data)
            return True
        except:
            Base.printErr("打开Excel文件失败！")
            return False
    #根据配置项目名称获取相应的值
    # page: excel sheet 名
    #items.字典型，获取字典中key对应的配置项值并返回结果字典
    #返回填充后的items
    def get_config_item(self, page, group, items):
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(page)
            nrows = table.nrows #行数

            bFound = False
            for num in range(0, nrows):
                row = table.row_values(num)
                if row:
                    if row[0] == '[%s]'%group:
                        bFound = True
                        continue
                    elif row[0][0:1]=="[":
                        bFound = False

                    if bFound:
                        for key in items.keys():
                            if key == row[0]:
                                items[key] = row[1]
            return items
        except:
            Base.printErr("获取Excel中配置信息失败！")
    #从键值对表格中根据名称获取对应的值
    # page: excel sheet 名
    #name：键值对中的键名
    #返回 对应的值
    def get_list_value(self, page, name):
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(page)
            nrows = table.nrows #行数

            for num in range(0, nrows):
                row = table.row_values(num)
                if row:
                    if row[0]==name:
                        return row[1]
            return None
        except:
            Base.printErr("获取Excel中键值对信息失败！")
    #获取页面中的全部数据
    #返回：全部数据，二维数组
    def get_page_data(self, page):
        try:
            if not self.open_excel():
                return None
            table = self.data.sheet_by_name(page)
            nrows = table.nrows #行数
            lists = []
            for num in range(0, nrows):
                row = table.row_values(num)
                if row:
                    lists.append(row)
            return lists
        except:
            Base.printErr("打开Excel中用例数据失败！")
    #将字符串中的"?"替换成对应的值
    #source:含“？”的原始字符串
    #vars：替换的值，一维数组
    def str_fill_parm(self, source, vars):
        try:
            if source.find("?") < 0: #如果没有需要替换的参数则直接返回源字串
                return source
            for var in vars:
                source = source.replace("?", "%s", 1)
                source = source%(var)
            return source
        except:
            Base.printErr("参数替换失败！")

    #解析函数格式：页名.函数名(参数1, 参数2，......)
    #func:函数字符串
    #返回替换后的字符串
    def str_parse_func(self, source):
        try:
            if source[0:1] == "$":
                source = source[1:]
            else:
                return source
            #func = "sql.delProduct(测试产品,服务类)"
            m = source.split(".")
            if len(m)==2:
                n = m[1].split("(")
                if len(n) == 2:
                    v = self.get_list_value(m[0], n[0])
                    n[1] = n[1].strip(" ")
                    n[1] = n[1].strip(")")
                    n[1] = n[1].strip()
                    xx = n[1].split(",")
                    yy = []
                    for x in xx:
                        x = x.strip()
                        yy.append(x)
                    s = self.str_fill_parm(v, yy)
                    return s

            raise RuntimeError("字符串格式错误:%s"%source)
        except:
            Base.printErr("解析函数字符串失败！")

    def write_by_index(self, row, col, page,value):
        try:
            self.target.get_sheet(page).write(row, col, value)
            return True
        except:
            Base.printErr("按行列号写入Excel文件失败！")
            return False

    def save_excel(self):
        try:
            self.target.save(self.targetName)
            return True
        except:
            Base.printErr("保存Excel文件失败！")
            return False

if __name__ == '__main__':
    ec = Excel("..\\..\\data\\RanzhiAutoCases.xlsx")
    dicDb = {"host":"", "port":"", "db":"", "user":"", "password":"", "charset":""}
    ec.get_config_item("config", "db", dicDb)
    print (dicDb)



    l= ec.get_page_data("login")
    print(l)

    f = "$sql.delProduct(测试产品)"
    s = ec.str_parse_func(f)
    print(s)