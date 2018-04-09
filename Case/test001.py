# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: web_function_Automation-Selenium
# author: "Lei Yong" 
# creation time: 2018/4/9 14:19
# Email: leiyong711@163.com

import unittest
from Operation.element import Element

el = Element()


class Test(unittest.TestCase):
    """火狐浏览器测试"""

    def setUp(self):
        self.driver = el.Driver()

    def testpassCase001(self):
        """百度搜索Python成功"""
        el.openurl("http://www.baidu.com")
        el.id("kw").send_keys("python")
        el.id("su").click()

    def testfailCase002(self):
        """百度搜索Python按钮点击失败"""
        el.openurl("http://www.baidu.com")
        el.id("kw").send_keys("python")
        el.id("su1").click()

    def tearDown(self):
        self.driver.quit()
