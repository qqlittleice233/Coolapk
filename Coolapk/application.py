import base64
import hashlib
import json
import os
import re
import time
from typing import Type
from urllib.parse import quote
import requests
from Coolapk.Exception import LoginError, LoginErrorAttributes, GetDataError, GetDataErrorAttributes
from Coolapk.object import Account, User
from Coolapk.utils import login


class CoolapkApplication:
    @staticmethod
    def login(account, password) -> Type[Account]:
        """
        调用login方法即可进行登录操作

        ps:如果请求次数过多，将会需要输入图形验证码 (出现此情况请更换ip再进行登录)
        :param account: 用户名、邮箱或手机号，海外手机号请务必带上区号(例子：+852-12345678)
        :param password: 账号密码
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
            quote('login', 'utf-8'): account,
            quote('password', 'utf-8'): password,
            quote('requestHash', 'utf-8'): quote(reqHash, 'utf-8'),
            quote('captcha', 'utf-8'): quote('', 'utf-8'),
            quote('randomNumber', 'utf-8'): quote(login.randomNumber(), 'utf-8')
        }
        req3 = requests.post("https://account.coolapk.com/auth/loginByCoolapk", headers=login_headers, cookies=cookies,
                             data=login_data)
        if len(req3.cookies.get('uid')) > 0 and len(req3.cookies.get('username')) > 0 and len(
                req3.cookies.get('token')) > 0:
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

    @staticmethod
    def __token() -> str:
        DEVICE_ID = "8513efac-09ea-3709-b214-95b366f1a185"
        t = int(time.time())
        hex_t = hex(t)
        # 时间戳加密
        md5_t = hashlib.md5(str(t).encode("utf-8")).hexdigest()
        # 不知道什么鬼字符串拼接
        a = "token://com.coolapk.market/c67ef5943784d09750dcfbb31020f0ab?{}${}&com.coolapk.market".format(
            md5_t, DEVICE_ID
        )
        # 不知道什么鬼字符串拼接 后的字符串再次加密
        md5_a = hashlib.md5(base64.b64encode(a.encode("utf-8"))).hexdigest()
        token = "{}{}{}".format(md5_a, DEVICE_ID, hex_t)
        return token

    @staticmethod
    def getUserData(uid: int) -> Type[User]:
        """
        该方法用于查询一个用户的数据，如果查询成功会返回一个User实例
        :param uid: 你要获得数据的uid
        :return: 返回一个User的实例
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 8 Lite Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 (#Build; Xiaomi; MI 8 Lite; QKQ1.190910.002 test-keys; 10) +CoolMarket/11.0.1',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Sdk-Int': '29',
            'X-Sdk-Locale': 'zh-CN',
            'X-App-Id': 'com.coolapk.market',
            'X-App-Token': CoolapkApplication.__token(),
            'X-App-Version': '11.0.1',
            'X-App-Code': '2102031',
            'X-Api-Version': '11',
            'X-App-Device': 'wOlRXaMBDOgkUTgsTat9WYphFI7kWbvFWaYByOEljO0YjOwUjOEdjOwEjOBlDI7AyOgsjN1YWMiJjN0QTOxEjZyYTO',
            'X-Dark-Mode': '1',
            'X-App-Channel': 'coolapk',
            'X-App-Mode': 'universal',
            'Host': 'api.coolapk.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}
        req = requests.get("https://api.coolapk.com/v6/user/space?uid={}".format(uid), headers=headers)
        data = json.loads(req.text)
        try:
            user = User
            user.uid = data['data']['uid']
            user.username = data['data']['username']
            user.admintype = data['data']['admintype']
            user.level = data['data']['level']
            user.experience = data['data']['experience']
            user.next_level_experience = data['data']['next_level_experience']
            user.next_level_percentage = data['data']['next_level_percentage']
            user.verify_title = data['data']['verify_title']
            user.verify_status = data['data']['verify_status']
            user.feed = data['data']['feed']
            user.follow = data['data']['follow']
            user.fans = data['data']['fans']
            return user
        except KeyError:
            raise GetDataError(GetDataErrorAttributes.KEY_ERROR)
