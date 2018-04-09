#Web UI功能自动化测试
#### 环境：
* * *
* selenium 2
* Python 2.7
* 火狐浏览器 47 以下版本（谷歌浏览器需安装对应版本驱动）
* * * 
 <br>
#### 描述：
* * *
* 该框架内包含测试完毕后自动发送邮件功能
* 测试报告包含测试失败截图
* * *
<br>

#### 用到的第三方的库（可能需自己安装）：
* * *
1.  email -- 4.0.2
2.  selenium -- 2.53.6
* * *
<br>
## 测试报告图片展示：
###测试报告默认状态
<br>
![image](https://raw.githubusercontent.com/leiyong711/web_function_Automation-Selenium/master/1.jpg)
<br>
###测试报告详情全部展开状态
![image](https://raw.githubusercontent.com/leiyong711/web_function_Automation-Selenium/master/2.jpg)
<br>
###用例例程：
<pre class="prettyprint lang-javascript">  
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


</pre>

<br>
### 封装常用元素定位方法
<pre class="prettyprint lang-javascript">
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

</pre>

<br>
<br>
<br>
##测试报告模板引用github上大神的，然后自己做了一下优化。[大神github地址](https://github.com/findyou)
<br>
<br>
<br>
