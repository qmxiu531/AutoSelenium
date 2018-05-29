import os
import sys
import smtplib
from email.header import Header
from email.mime.text import MIMEText

class Base(object):
    @staticmethod
    def printErr(userInfo="", bPrint=True):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = "异常类型：%s, 在 %s 的第 %d 行；%s"%(exc_type, fname, exc_tb.tb_lineno, exc_obj)
        if userInfo:
            msg = msg + "\n" + userInfo
        if bPrint:
            print(msg)
        return msg

    #获取file所在的当前路径
    @staticmethod
    def get_cur_dir(file):
        return os.path.split(os.path.realpath(file))[0]

    @staticmethod
    def send_email(targetEmail, reportFile):
        """
        发送邮件
        :param targetEmail:
        :return:
        """

        # 打开测试报告结果
        # r:read
        # b:binary
        try:
            f = open(reportFile, "rb")

            # 将测试结果放到邮件的主体中
            mail_body = f.read()
            # 关闭测试结果的文件
            f.close()

            # 声明一个邮件对象，用刚刚得到的邮件主体
            msg = MIMEText(mail_body, "html", "utf-8")
            # 设置邮件的主题
            msg["subject"] = Header("Selenium自动化测试结果", "utf-8")
            # 创建一个SMTP服务对象
            # simple message transfer protocol
            # 简单的消息转移协议
            smtpMail = smtplib.SMTP()

            # 连接SMTP的服务器
            #smtp.163.com
            smtpMail.connect("smtp.21cn.com")

            emailFrom = "selenium2@21cn.com"
            password = "Welcome123"
            # 登录SMTP的服务器
            smtpMail.login(emailFrom, password)

            # 使用SMTP的服务器发送邮件
            smtpMail.sendmail(emailFrom, targetEmail, msg.as_string())

            # 退出SMTP对象
            smtpMail.quit()
        except:
            Base.printErr("邮件发送失败！")

    @staticmethod
    def listToDic(listKey, listValue):
        rDic = {}
        try:
            i = 0
            for li in listKey:
                rDic[li] = listValue[i]
                i += 1
        except:
            Base.printErr("数组生成字典失败！")
        return rDic
#if __name__ == "__main__":
    #Base.readConfig()