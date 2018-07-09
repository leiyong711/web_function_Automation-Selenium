# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project name: CP_Automation
# author: "Lei Yong" 
# creation time: 2018/7/6 14:39
# Email: leiyong711@163.com

import requests


def code_demo(username, password, image, typeid, timeout=60):
    # 验证码类型(typeid)1**0 纯数字,2**0 纯英文,3**0 英文数字混合,4**0 纯汉字,5000数字英文汉字混合
    # (*000任意长度混合,*010-*100对应1-10位组合)）

    # 制作协议包
    data = {'username': username,
            'password': password,
            'softid': '84583',
            'softkey': '7b891f29bbad4e009d473e319db4e1c0',
            'typeid': typeid,
            'timeout': timeout}

    header = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    # 发送Post请求
    im = open(image, 'rb').read()
    files = {'image': ('verificationCode.png', im)}
    req = requests.post('http://api.ruokuai.com/create.json', data=data, files=files, headers=header)

    # 获得结果
    qrcont = req.json()
    try:
        return qrcont['Result']
    except:
        return qrcont['Error']

if __name__ == '__main__':
    print(code_demo('', '', '', ''))  # 参数（用户名，密码，图片地址，验证码类型）
