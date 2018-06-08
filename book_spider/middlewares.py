# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64

from scrapy import signals
from settings import User_Agents
from settings import PROXIES


class RandomUserAgent(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self,request,spider):
        useragent = random.choice(User_Agents)
        # 把User-Agent添加到请求头中
        print useragent
        request.headers.setdefault('User-Agent',useragent)


class RandomProxy(object):
    """docstring for ClassName"""
    def process_request(self,request,spider):
        proxy = random.choice(PROXIES)

        # 把代理ip保存到元数据里面，因为ip属于元数据
        if proxy['user_passwd'] is None:
            #没有账号验证的
            request.meta['proxy'] = 'http://' + proxy['ip_port']
        else:
            # 账号和密码进行base64转换
            base64_userPasswd = base64.b64encode(proxy['user_passwd'])
            # 设置ip
            request.meta['proxy'] = 'http://' + proxy['ip_port']
            # 设置ip账号密码，Basic 要加个空格
            request.headers['Proxy-Authorization'] = 'Basic ' + base64_userPasswd
