# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: CP v1.3.1
# author: "Lei Yong" 
# creation time: 2018/4/9 10:10
# Email: leiyong711@163.com

import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def mail(recipient='leiyong711@163.com'):
    sender = ''  # 发件人邮箱
    my_pass = ''  # 授权码
    toRecipient = recipient.split(",")

    # 创建一个带附件的实例
    msg = MIMEMultipart()
    msg['From'] = Header("WEB自动化测试报告 <%s>" % "雷勇", 'utf-8')  # 显示的发件人
    msg['To'] = ",".join(toRecipient)  # 显示多个发件人
    msg['Subject'] = Header("自动化测试报告", "utf-8")  # 邮件主题

    # 附件名字与路径
    cur_path = os.path.dirname(os.path.realpath(__file__))[:-9]
    timeStr = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    attachmentPath = cur_path + 'Report\\' + timeStr[:10] + '\\' + timeStr[11:] + '\\'

    attachmentTemp = os.listdir(attachmentPath)
    for i in range(len(attachmentTemp)):
        if str(attachmentTemp[i]).find(".html") != -1:
            attachmentName = attachmentTemp[i]

    # 邮件正文内容
    bodyContent = "以下是执行后的测试报告：\n   • %s" % attachmentName
    msg.attach(MIMEText(bodyContent, "plain", "utf-8"))

    # 构建附件，发送当前目录下的HTML测试报告文件
    att = MIMEText(open(attachmentPath + attachmentName, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=' + attachmentName
    msg.attach(att)

    try:
        # server = smtplib.SMTP("smtp.aliyun.com", 25)  # 发件人邮箱中的'SMTP'服务器，端口是25
        server = smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的'SMTP'服务器，端口是25
        server.login(sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码

        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(sender, toRecipient, msg.as_string())
        # 关闭连接
        server.quit()
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("无法发送邮件")


if __name__ == "__main__":
    mail("leiyonghn@163.com,1804882096@qq.com")
