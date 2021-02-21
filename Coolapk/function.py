import json
import re
from typing import Type
from urllib.parse import quote
from Coolapk.utils import login
import requests
from Coolapk.Exception import LoginError, LoginErrorAttributes
import os
from Coolapk.object import Account


class Login:
    def __init__(self, account, password):
        """
        创建Login实例后调用get方法即可进行登录操作

        ps:如果请求次数过多，将会需要输入图形验证码 (出现此情况请更换ip再进行登录)
        :param account: 用户名、邮箱或手机号，海外手机号请务必带上区号(例子：+852-12345678)
        :param password: 账号密码
        """
        self.__randomNumber = login.randomNumber()
        self.__account = account
        self.__password = password

    def get(self) -> Type[Account]:
        """
        调用此方法进行登录操作
        :return: 如果登录成功，返回一个Account实例
        """
        if os.path.exists(".\\key.coolapk"):
            return login.readKeyFile()
        headers = {
            'Host': 'account.coolapk.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 8 Lite Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 (#Build; Xiaomi; MI 8 Lite; QKQ1.190910.002 test-keys; 10) +CoolMarket/10.4',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'X-Requested-With': 'com.coolapk.market',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        req = requests.get("https://account.coolapk.com/auth/login?type=coolapk", headers=headers)
        sessid = req.cookies.get("SESSID")
        forward = req.cookies.get("forward")
        if len(sessid) == 0:
            raise LoginError(LoginErrorAttributes.SESSID_NOT_FOUND)
        if len(forward) == 0:
            raise LoginError(LoginErrorAttributes.FORWARD_NOT_FOUND)

        cookies = {
            "SESSID": sessid,
            "forward": forward
        }
        req2 = requests.get("https://account.coolapk.com/auth/loginByCoolapk", headers=headers, cookies=cookies)
        reqHash = re.findall("requestHash : '(.*)',", req2.text)[0]
        if len(reqHash) == 0:
            raise LoginError(LoginErrorAttributes.REQHASH_NOT_FOUND)

        login_headers = {
            'Host': 'account.coolapk.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 8 Lite Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 (#Build; Xiaomi; MI 8 Lite; QKQ1.190910.002 test-keys; 10) +CoolMarket/10.4',
            'x-requested-with': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://account.coolapk.com',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://account.coolapk.com/auth/loginByCoolapk',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': '*/*',

        }
        login_data = {
            quote('submit', 'utf-8'): quote('1', 'utf-8'),
            quote('login', 'utf-8'): self.__account,
            quote('password', 'utf-8'): self.__password,
            quote('requestHash', 'utf-8'): quote(reqHash, 'utf-8'),
            quote('captcha', 'utf-8'): quote('', 'utf-8'),
            quote('randomNumber', 'utf-8'): quote(login.randomNumber(), 'utf-8')
        }
        req3 = requests.post("https://account.coolapk.com/auth/loginByCoolapk", headers=login_headers, cookies=cookies, data=login_data)
        if len(req3.cookies.get('uid')) > 0 and len(req3.cookies.get('username')) > 0 and len(req3.cookies.get('token')) > 0:
            account = Account
            account.uid = req3.cookies.get("uid")
            account.username = req3.cookies.get("username")
            account.token = req3.cookies.get("token")
            login.writeKeyFile(account)
            print("登录成功")
            return account
        else:
            print("登录异常")
            print(json.loads(req3.text))
