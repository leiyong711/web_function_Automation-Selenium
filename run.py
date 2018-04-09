# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: web_function_Automation-Selenium
# author: "Lei Yong" 
# creation time: 2018/4/9 14:20
# Email: leiyong711@163.com

import sys
import unittest
import platform
import HTMLTestRunnertest
from Operation.e_mail import *

reload(sys)
sys.setdefaultencoding('utf8')

cur_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
case_path = os.path.join(cur_path, "Case")        # 测试用例的路径

# 创建多级目录，以便存放最终测试报告
timeStr = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
path = 'Report\\' + timeStr[:10] + '\\' + timeStr[11:]
try:
    os.makedirs(path)
    print("文件目录不存在，正在创建...")
except:
    print("文件目录已存在，不需重新创建。")

report_path = os.path.join(cur_path, path)  # 报告存放路径


if __name__ == "__main__":
    # 自动添加Case目录下所有符合test*.py的用例
    testCase = unittest.defaultTestLoader.discover(case_path, "test*.py")
    run = HTMLTestRunnertest.HTMLTestRunner(title="Web自动化测试报告",
                                            description="测试环境：%s、python %s、Selenium2、火狐浏览器47.0.1" % (platform.platform(), platform.python_version()),
                                            tester="最棒QA",  # 测试人员姓名
                                            stream=open(report_path+"\\ TestReport.html", "wb"),
                                            verbosity=1.1)

    run.run(testCase)
    time.sleep(5)
    mail("leiyong711@163.com,1804882096@qq.com")
