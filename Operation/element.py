# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: CP_Automation
# author: "Lei Yong"
# creation time: 2018/7/5 17:17
# Email: leiyong711@163.com

import time
from log_config.logConfig import logger
from selenium import webdriver
from PIL import Image
from Operation.verificationCode import code_demo

# c = 0


class Element(object):
    # def __init__(self):
    #     self.driver = webdriver.Chrome()  # 测试执行浏览器选择
    #     # self.driver = webdriver.Firefox()
    #     if c == 0:
    #         self.driver.quit()

    # 关闭首次打开的浏览器
    # def Driver(self):
    #     global c
    #     c = 5
    #     self.__init__()
    #     return self.driver

    # 初始化
    def Driver(self):
        self.driver = webdriver.Chrome()
        return self.driver

###################################
#           浏览器操作             #
###################################

    # 打开网页
    def openurl(self, url):
        logger.info("打开网页：%s" % url)
        # print("打开网页：%s" % url)
        self.driver.get(url)

    # 关闭浏览器
    def quit(self):
        # print("关闭浏览器")
        logger.info("关闭浏览器")
        self.driver.quit()

    # 浏览器最大化
    def windowMax(self):
        # print("浏览器最大化")
        logger.info("浏览器最大化")
        self.driver.maximize_window()

    # 自定义浏览器大小
    def customWindow(self, wide, hige):
        # print("设置浏览器宽高：%s, %s" % (wide,hige))
        logger.info("设置浏览器宽高：%s, %s" % (wide, hige))
        self.driver.set_window_size(wide, hige)

    # 浏览器前进
    def forward(self):
        # print("浏览器前进")
        logger.info("浏览器前进")
        self.driver.forward()

    # 浏览器后退
    def back(self):
        # print("浏览器后退")
        logger.info("浏览器后退")
        self.driver.back()

    # 删除指定cookie
    def rm_cooke(self, cooke):
        logger.info("删除浏览器 %s Cookie" % cooke)
        self.driver.delete_cookie(cooke)

    # 删除所有cookie
    def rm_all_cooke(self):
        logger.info("删除浏览器所有Cookie")
        self.driver.delete_cookie()


###################################
#           元素定位操作           #
###################################

    # Name 元素定位
    def name(self, value):
        # print("Name 元素定位：%s"% value)
        logger.info("Name 元素定位：%s" % value)
        return self.driver.find_element_by_name(value)

    # class Name 元素定位
    def className(self, value):
        # print("className 元素定位：%s" % value)
        logger.info("className 元素定位：%s" % value)
        return self.driver.find_element_by_class_name(value)

    # Id 元素定位
    def id(self, value):
        # print("Id 元素定位：%s" % value)
        logger.info("Id 元素定位：%s" % value)
        return self.driver.find_element_by_id(value)

    # css 元素定位
    def css(self, value):
        # print("Css 元素定位：%s" % value)
        logger.info("Css 元素定位：%s" % value)
        return self.driver.find_element_by_css_selector(value)

    # Text 元素定位
    def text(self, value):
        # print("Text 元素定位：%s" % value)
        logger.info("Text 元素定位：%s" % value)
        return self.driver.find_element_by_link_text(value)

    # Xpath
    def xpath(self, value):
        # print("Xpath 元素定位：%s" % value)
        logger.info("Xpath 元素定位：%s" % value)
        return self.driver.find_element_by_xpath(value)

###################################
#        获取元素大小尺寸          #
###################################

    # 获取id元素大小
    def id_size(self, id):
        num = self.driver.find_element_by_id(id).size
        logger.info("获取id元素大小   %s  大小：%s" % (id, num))
        return num

    # 获取name元素大小
    def name_size(self, name):
        num = self.driver.find_element_by_id(name).size
        logger.info("获取name元素大小   %s  大小：%s" % (name, num))
        return num

    # 获取css元素大小
    def css_size(self, css):
        num = self.driver.find_element_by_id(css).size
        logger.info("获取css元素大小   %s  大小：%s" % (css, num))
        return num

    # 获取xpath元素大小
    def xpath_size(self, xpath):
        num = self.driver.find_element_by_id(xpath).size
        logger.info("获取xpath元素大小   %s  大小：%s" % (xpath, num))
        return num

###################################
#         获取元素文本值           #
###################################

    # 获取id文本
    def get_id_text(self, id):
        num = self.driver.find_element_by_id(id).text
        logger.info("获取id元素值：%s 值为 %s" % (id, num))
        return num

    # 获取name文本
    def get_name_text(self, name):
        num = self.driver.find_element_by_id(name).text
        logger.info("获取name元素值：%s 值为 %s" % (name, num))
        return num

    # 获取xpath文本
    def get_xpath_text(self, xpath):
        num = self.driver.find_element_by_xpath(xpath).text
        logger.info("获取xpath元素值：%s 值为 %s" % (xpath, num))
        return num

    # 获取css文本
    def get_css_text(self, css):
        num = self.driver.find_element_by_css_selector(css).text
        logger.info("获取css元素值：%s 值为 %s" % (css, num))
        return num

###################################
#            断言                 #
###################################

    # 判断元素是否存在
    def is_element_exist(self, func):
        s = func
        if len(s) == 0:
            # print("元素未找到：%s" % value)
            logger.info("判断元素是否存在:  元素未找到：%s" % func)
            return False
        elif len(s) == 1:
            # print("元素：%s 已找到" % value)
            logger.info("判断元素是否存在:  元素：%s 已找到" % func)
            return True
        else:
            # print("找到%s个元素：%s" % value)
            logger.info("判断元素是否存在:  找到%s个元素：%s" % func)
            return False

    # 判断元素是否存在
    def isElementExist(self, func):
        try:
            func
            logger.info("判断元素是否存在:   找到%s元素：%s" % func)
            return True
        except:
            logger.info("判断元素是否存在:   元素未找到：%s" % func)
            return False

    # 显式等待断言
    def trywait_assert(self, func, count=3):
        num = 0
        while num != count:
            logger.error('%s' % str(num))
            logger.error('jinlailo ')
            try:
                func
                return True
            except:
                logger.info("等待断言:   %s:元素未找到,当前第%s次寻找" % (func, num))
                num += 1
                time.sleep(0.5)
        return False

    # xpath 断言等待
    def trywait_assert_xpath(self, func, count=3):
        num = 0
        while num != count:
            try:
                self.driver.find_element_by_xpath(func)
                return True
            except:
                logger.info("等待断言:   %s:元素未找到,当前第%s次寻找" % (func, num + 1))
                num += 1
                time.sleep(0.5)
        return False

###################################
#            等待                 #
###################################

    # 隐式等待
    def citlyWait(self, ti):
        logger.info("隐式等待 %s 秒" % ti)
        self.driver.implicitly_wait(ti)

    # 显式等待
    def trywait(self, func, count=3):
        num = 0
        while num != count:
            try:
                return func
            except:
                logger.info("显式等待:  %s:元素未找到,当前第%s次寻找" % (func, num))
                num += 1
                time.sleep(0.5)

    # 彩票封盘等待
    def cp_trywait(self, css1, css2):
        state = self.driver.find_element_by_css_selector(css1).text
        seconds = self.driver.find_element_by_css_selector(css2).text
        logger.info(state, seconds)
        if state[-2:] == u"截止" and int(seconds) >= 20:
            logger.info("当前状态 {}  时间 {}".format(state, seconds))
        else:
            time.sleep(int(seconds) + 2)
            logger.info("封盘中！ 等待 {} s".format(seconds))

    # 验证码识别
    def get_verificationCode(self, func):
        self.driver.save_screenshot('img\\verificationCode.png')
        element = func
        logger.info("获取图片元素坐标 {}".format(element.location))
        logger.info("获取图片元素大小 {}".format(element.size))

        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']

        im = Image.open('img\\verificationCode.png')
        im = im.crop((left, top, right, bottom))
        im.save('img\\verificationCode.png')

        value = code_demo('', '', 'img\\verificationCode.png', '7100')  # 请输入若快账户密码
        logger.info("若快识别结果为    {}".format(value))
        return value
