# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: web_function_Automation-Selenium
# author: "Lei Yong" 
# creation time: 2018/4/9 14:16
# Email: leiyong711@163.com
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: iOS_Ui_Automation
# author: "Lei Yong"
# creation time: 2018/1/9 下午5:46
# Email: leiyong711@163.com

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: huibao_v2.0
# author: "Lei Yong"
# creation time: 2017/8/10 0010 22:24
# Email: leiyong711@163.com

"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.
The simplest way to use this is to invoke its main method. E.g.
    import unittest
    import HTMLTestRunner
    ... define your tests ...
    if __name__ == '__main__':
        HTMLTestRunner.main()
For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.
    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )
    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'
    # run the test
    runner.run(my_test_suite)
------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung,  Findyou"
__version__ = "0.8.2.1"


"""
Change History
Version 0.8.2.1 -Findyou
* 支持中文，汉化
* 调整样式，美化（需要连入网络，使用的百度的Bootstrap.js）
* 增加 通过分类显示、测试人员、通过率的展示
* 优化“详细”与“收起”状态的变换
* 增加返回顶部的锚点
Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).
Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.
Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.
Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?
import os
import datetime
import StringIO
import sys
import time
import unittest
from xml.sax import saxutils
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

leiyong123 = 0

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.
    Overall structure of an HTML report
    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
    0: '通过',
    1: '失败',
    2: '错误',
    }

    DEFAULT_TITLE = '单元测试报告'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_TESTER='最棒QA'

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    %(stylesheet)s
</head>
<body >
<script language="javascript" type="text/javascript">
output_list = Array();
/*level 调整增加只显示通过用例的分类 --Findyou
0:Summary //all hiddenRow
1:Failed  //pt hiddenRow, ft none
2:Pass    //pt none, ft hiddenRow
3:All     //pt none, ft none
*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }
    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}
function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}
function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
%(heading)s
%(report)s
%(ending)s
</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)


    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 100%; }
table       { font-size: 100%; }
/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1 style="font-family: Microsoft YaHei">%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>
""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong style="font-size: 18px">%(name)s : </strong> <span style=" font-size: 15px">%(value)s</p>
""" # variables: (name, value)



    # ------------------------------------------------------------------------
    # Report
    #
    # 汉化,加美化效果 --Findyou
    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" href='javascript:showCase(0)'>概要{ %(passrate)s }</a>
<a class="btn btn-danger" href='javascript:showCase(1)'>失败{ %(fail)s }</a>
<a class="btn btn-success" href='javascript:showCase(2)'>通过{ %(Pass)s }</a>
<a class="btn btn-info" href='javascript:showCase(3)'>所有{ %(count)s }</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 22px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <td>错误</td>
    <td>详细</td>
    <td>截图</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>%(count)s</td>
    <td>通过率：%(passrate)s</td>
</tr>
</table>
""" # variables: (test_list, count, Pass, fail, error ,passrate)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s warning' style="font-size: 16px">
    <td>%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
    <td class="text-center">%(error)s</td>
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
    <td class="text-center">%(count)s</td>
</tr>
""" # variables: (style, desc, count, Pass, fail, error, cid)

    #失败 的样式，去掉原来JS效果，美化展示效果  -Findyou
    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s' style="font-size: 14px">
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>
    <!--默认收起错误信息 -Findyou -->
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s' style="%(kt)s">%(status)s</button>
    <div id='div_%(tid)s' class="collapse">
    <!-- 默认展开错误信息 -Findyou
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse in"> -->
    <pre>
    %(script)s
    </pre>
    </div>
    </td>

    <td colspan='5_' align='center'>
    <button id='btn_%(tid)s_' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s_' style="%(kt)s">截图</button>
    <div id='div_%(tid)s_' class="collapse">
    <pre>
    %(screenshot)s
    </pre>
    </div>
    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)

    # 通过 的样式，加标签效果  -Findyou
    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s' style="font-size: 15px">
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'><span class="btn btn-success btn-xs collapsed" style="padding: 1px 5px;font-size: 12px;line-height: 1.5;border-radius: 3px;background-color: #5cb85c;border: 1px solid #5cb85c;color:#fff">%(status)s</span></td>

    <td colspan='5_' align='center'>
    <button id='btn_%(tid)s_' type="button"  class="btn btn-success btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s_' style="0">截图</button>
    <div id='div_%(tid)s_' class="collapse">
	<pre>
    <img src="%(screenshot)s" width="272px" height="262px"/>
    </pre>
    </div>
    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #
    # 增加返回顶部按钮  --Findyou
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:60px;" aria-hidden="true">
    </span></a></div>
    """

# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult

class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        #增加一个测试通过率 --Findyou
        self.passrate=float(0)


    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector


    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        self.status = 0
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')


    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        try:
            driver = getattr(test, "driver")
            test.img = 'data:image/jpg;base64,%s' % driver.get_screenshot_as_base64()
        except AttributeError:
            test.img = ""
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')


    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        try:
            driver = getattr(test, "driver")
            test.img = 'data:image/jpg;base64,%s' % driver.get_screenshot_as_base64()
        except AttributeError:
            test.img = ""
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')
        # print test.img


class HTMLTestRunner(Template_mixin):
    """
    """
    def __init__(self, stream=sys.stdout, verbosity=1,title=None,description=None,tester=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester

        self.startTime = datetime.datetime.now()


    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
        print >>sys.stderr, '\nTime Elapsed: %s' % (self.stopTime-self.startTime)
        return result


    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n,t,o,e in result_list:
            cls = t.__class__
            if not rmap.has_key(cls):
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    #替换测试结果status为通过率 --Findyou
    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        status.append('共 %s' % (result.success_count + result.failure_count + result.error_count))
        if result.success_count: status.append('通过 %s'    % result.success_count)
        if result.failure_count: status.append('失败 %s' % result.failure_count)
        if result.error_count:   status.append('错误 %s'   % result.error_count  )
        if status:
            status = '，'.join(status)
            self.passrate = str("%.2f%%" % (float(result.success_count) / float(result.success_count + result.failure_count + result.error_count) * 100))
        else:
            status = 'none'
        return [
            (u'测试人员', self.tester),
            (u'开始时间',startTime),
            (u'合计耗时',duration),
            (u'测试结果',status + "，通过率= "+self.passrate),
        ]


    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            report = report,
            ending = ending,
        )
        self.stream.write(output.encode('utf8'))


    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    #增加Tester显示 -Findyou
    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
            tester= saxutils.escape(self.tester),
        )
        return heading

    #生成报告  --Findyou添加注释
    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            for n,t,o,e in cls_results:
                if n == 0: np += 1
                elif n == 1: nf += 1
                else: ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row = self.REPORT_CLASS_TMPL % dict(
                style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc = desc,
                count = np+nf+ne,
                Pass = np,
                fail = nf,
                error = ne,
                cid = 'c%s' % (cid+1),
            )
            rows.append(row)

            for tid, (n,t,o,e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            count = str(result.success_count+result.failure_count+result.error_count),
            Pass = str(result.success_count),
            fail = str(result.failure_count),
            error = str(result.error_count),
            passrate =self.passrate,
        )

        global leiyong123
        count2 = str(result.success_count + result.failure_count + result.error_count)
        Pass2 = str(result.success_count)
        fail2 = str(result.failure_count)
        error2 = str(result.error_count)
        leiyong123 = [count2, Pass2, fail2, error2]

        return report


    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        # ID修改点为下划线,支持Bootstrap折叠展开特效 - Findyou
        tid = (n == 0 and 'p' or 'f') + 't%s_%s' % (cid+1,tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # utf-8 支持中文 - Findyou
         # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            # uo = o.decode('latin-1')
            uo = o.decode('utf-8')
        else:
            uo = o
        if isinstance(e, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            # ue = e.decode('latin-1')
            ue = e.decode('utf-8')
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id = tid,
            output = saxutils.escape(uo+ue),
        )
        if self.STATUS[n] == '通过':
            kt1 = 'padding: 1px 5px;font-size: 12px;line-height: 1.5;border-radius: 3px;background-color: #5cb85c;border: 1px solid #5cb85c;color:#fff'
            # kt1 = ''
        else:
            kt1 = '0'

        # print 8888888888
        # print type(t)
        # print t
        # print type(t.img)
        # print t.img
        # print self.STATUS[n]
        if self.STATUS[n] != '通过':
            screenshot_a = '<img src="%s" width="960px" height="640px" />' % t.img

        else:
            screenshot_a = '<img src="data:image/jpeg;base64,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" width="272px" height="262px" />'

        row = tmpl % dict(
            tid = tid,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
            desc = desc,
            script = script,
            status = self.STATUS[n],
            screenshot=screenshot_a,
            kt = kt1,
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL

    # def screenshot(self):
    #     timee = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
    #     img_path = '..\\report\\%s\\%s\\er_img\\' % (timee[:10], timee[11:])
    #     timestr = time.strftime('%Y%m%d',time.localtime(time.time()))
    #     global index
    #     count = 0
    #     while count < 100:
    #         lsdir = os.listdir(img_path)
    #         img_name = timestr + '_' + str(index) + '.jpg'
    #         if img_name in lsdir:
    #             index+=1
    #             return '..\\er_img\\%s' % img_name
    #         else:
    #             time.sleep(0.0001)
    #             index += 1
    #             count += 1
    #     return 'http://39.108.101.214/error.jpg'


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """
    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)

main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
