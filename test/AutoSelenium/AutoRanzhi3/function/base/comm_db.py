# -*- coding: utf-8 -*-
import pymysql          #导入pymysql.py的包
from function.base.base import *
"""
class ranzhi_db
作者：David
时间：
方法：execSql:1、可执行删除等操作；2、可执行验证SQL语句
"""
class CommonDB(object):
    '''
    方法：构造函数，初始化数据库连接参数
    入参：
        host: mysql主机名或IP
        ....
    输出：转换为类成员变量
    '''
    def __init__(self, host, port, db, user, passwd, charset):
        self.m_host = host
        self.m_port = port
        self.m_db = db
        self.m_user = user
        self.m_passwd = passwd
        self.m_charset = charset
    '''
    方法：execSql:1、可执行删除等操作；2、可执行验证SQL语句; 3、可执行通用查询操作
    入参：
        strSql: 需要执行的SQL语句串
        bVerify:执行的语句是否为验证SQL；True/False
    输出：rc[A,B]
        A：SQL语句是否执行成功；True/False
        B: 返回数据；
            1、如果bVerify==True,返回第一行第一列的数据
            2、None（如果没有数据返回）
            3、其他正常的SQL返回信息
            4、如果SQL执行失败，则返回错误信息
    '''
    def execSql(self, strSql, bVerify=False):
        rc = [True, ""]
        try:
            #获取数据库连接，使用参数
            conn = pymysql.connect(host=self.m_host,port=self.m_port,
                                   user=self.m_user,passwd=self.m_passwd,
                                   db=self.m_db,charset=self.m_charset)
            cur = conn.cursor()     #获取一个游标
            cur.execute(strSql)     #执行一条数据库查询语句
            data = cur.fetchall()   #将执行结果返回给data,data是一个二维数组
            #无执行错误表示SQL执行成功
            if bVerify: #执行的是验证语句
                rc[0] = True        #表示sql语句执行成功
                rc[1] = data[0][0]  #SQL语句返回的第一行第一列数据赋值给返回数组
            elif len(data) >= 1:#   如果返回的数据大于一行，且不是执行的验证SQL
                rc[0] = True        #表示sql语句执行成功
                rc[1] = data         #SQL语句返回全部数据，是一个二维数组
            else:                   #如果没有返回数据
                rc[0] = True        #表示sql语句执行成功
                rc[1] = None        #数据赋值为None
            cur.execute("commit;")          #执行一条数据库提交语句
            cur.close()
            conn.close()
        except:
            rc[0] = False                           #数据库操作失败了
            rc[1] = Base.printErr("\n\t数据库操作失败：%s"%strSql, False)#错误提示信息是什么
            try:
                conn.close()
            except Exception as ee:
                pass
        return rc

if __name__ == '__main__':
    #练习一个验证SQL，rc[1]返回数据一定是1或0
    mysqlExec = CommonDB("127.0.0.1", 3306, "ranzhi", "root", "", "utf8")

    strSql = "select count(*)=1 from sys_product where name='51测试产品' " \
             "and status='normal' and type='service' and line='cc';"
    rc = mysqlExec.execSql(strSql, True)
    print (rc)

    #练习一个普通查询，rc[1]返回数据一定是一个二维数组
    strSql = "select * from sys_product;"
    rc = mysqlExec.execSql(strSql)
    print (rc)
    #练习一个更新操作，rc[1]没有返回数据
    strSql = "UPDATE sys_product SET NAME='自动化测试产品' WHERE id=25 ;"
    rc = mysqlExec.execSql(strSql)
    print (rc)
