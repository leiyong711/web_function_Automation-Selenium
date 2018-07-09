# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: CP v1.3.1
# author: "Lei Yong" 
# creation time: 2018/6/27 15:24
# Email: leiyong711@163.com

import os
import logging.config
path = os.path.dirname(os.path.realpath(__file__))
print(path)



logging.config.fileConfig("%s/logger.conf" % path)
logger = logging.getLogger("root")


if __name__ == "__main__":
    # logger = log()
    logger.error('错误咯')
    logger.info('运行日志')
    logger.debug('调试日志')
    logger.warning('不知道')
    logger.critical('不懂')
