# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: web_function_Automation-Selenium
# author: "Lei Yong" 
# creation time: 2018/4/9 14:17
# Email: leiyong711@163.com

import time
from selenium import webdriver

c = 0


class Element(object):

    def __init__(self):

        self.driver = webdriver.Firefox()
        if c == 0:
            self.driver.quit()

    def Driver(self):
        global c
        c = 5
        self.__init__()
        return self.driver

    # 打开网页
    def openurl(self, url):
        print("打开网页：%s" % url)
        self.driver.get(url)

    # 关闭浏览器
    def quit(self):
        print("关闭浏览器")
        self.driver.quit()

    # 浏览器最大化
    def windowMax(self):
        print("浏览器最大化")
        self.driver.maximize_window()

    # 自定义浏览器大小
    def customWindow(self, wide, hige):
        print("设置浏览器宽高：%s, %s" % (wide,hige))
        self.driver.set_window_size(wide, hige)

    # 浏览器前进
    def forward(self):
        print("浏览器前进")
        self.driver.forward()

    # 浏览器后退
    def back(self):
        print("浏览器后退")
        self.driver.back()

    # Name 元素定位
    def name(self, value):
        print("Name 元素定位：%s"% value)
        return self.driver.find_element_by_name(value)

    # class Name 元素定位
    def className(self, value):
        print("className 元素定位：%s" % value)
        return self.driver.find_element_by_class_name(value)

    # Id 元素定位
    def id(self, value):
        print("Id 元素定位：%s" % value)
        return self.driver.find_element_by_id(value)

    # css 元素定位
    def css(self, value):
        print("Css 元素定位：%s" % value)
        return self.driver.find_element_by_css_selector(value)

    # Text 元素定位
    def text(self, value):
        print("Text 元素定位：%s" % value)
        return self.driver.find_element_by_link_text(value)

    # Xpath
    def xpath(self, value):
        print("Xpath 元素定位：%s" % value)
        return self.driver.find_element_by_xpath(value)

    # 判断元素是否存在
    def is_element_exist(self, value):
        s = self.driver.find_element_by_name(value)
        if len(s) == 0:
            print("元素未找到：%s" % value)
            return False
        elif len(s) == 1:
            print("元素：%s 已找到" % value)
            return True
        else:
            print("找到%s个元素：%s" % value)
            return False

    # 判断元素是否存在
    def isElementExist(self, value):
        try:
            self.driver.find_element_by_name(value)
            return True
        except:
            return False

    # 隐式等待
    def citlyWait(self, ti):
        self.driver.implicitly_wait(ti)

    # 显式等待
    def trywait(self, value, count=3):
        while count:
            try:
                self.driver.find_element_by_name(value)
                break
            except:
                print("%s:元素未找到,当前第%s次寻找" % (value, count))
                count += 1
                time.sleep(0.5)
