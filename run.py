# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: CP v1.3.1
# author: "Lei Yong" 
# creation time: 2018/4/8 14:05
# Email: leiyong711@163.com
import os
import unittest
import platform
from log_config.logConfig import logger
from Operation.e_mail import *
from Operation.element import Element

el = Element()
el = el.Driver()

#  获取当前python版本
pythonVersions = platform.python_version()
# 按版本自动调用对应测试报告模板
if float(pythonVersions[:3]) > 2.7:
    import HTMLTestRunner_py3 as HTMLTestRunner
else:
    import HTMLTestRunner as HTMLTestRunner

    # reload(sys)
    # sys.setdefaultencoding('utf8')

cur_path = os.path.dirname(os.path.realpath(__file__))
case_path = os.path.join(cur_path, "Case")        # 测试用例的路径


def mkfile():
    timeStr = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    path = 'Report\\' + timeStr[:10] + '\\' + timeStr[11:]
    try:
        os.makedirs(path)
        print('\033[1;31m' + u'文件目录不存在，正在创建...' + '\033[0m')
    except:
        print('\033[1;31m' + u'文件目录已存在，不需重新创建。' + '\033[0m')

    return os.path.join(cur_path, path)  # 报告存放路径


if __name__ == "__main__":
    report_path = mkfile()
    discover = unittest.defaultTestLoader.discover(case_path, "*.py")  # 自动测试该文件夹下所有用例，如要单独执行则如：test001.py
    run = HTMLTestRunner.HTMLTestRunner(title="CP项目自动化测试报告",
                                        description="测试环境：{}、python {}、Selenium2、{}：{}" .format(platform.platform(), pythonVersions,
                                                                                                el.capabilities['browserName'],
                                                                                                el.capabilities['version']),
                                        tester="最棒QA",
                                        stream=open(report_path+"\\ TestReport.html", "wb"),
                                        verbosity=1.1)
    el.quit()  # 关闭多余浏览器
    run.run(discover)
    time.sleep(5)
    mail("leiyonghn@163.com,leiyong711@163.com,1804882096@qq.com")
    logger.info('向"leiyonghn@163.com,leiyong711@163.com,1804882096@qq.com" 发送测试报告邮件')
    logger.info("测试结束")
