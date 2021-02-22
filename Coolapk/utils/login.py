from random import choice
from typing import Type
from Coolapk.object import Account
import base64
import string
from Coolapk.Exception import LoginError, LoginErrorAttributes


def randomNumber():
    """

    :return: 返回酷安登录所需的随机数
    """
    number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    randomNumber = '0undefined'
    make = [16, 17, 18]
    for i in range(0, choice(make)):
        randomNumber = randomNumber + str(choice(number))
    return randomNumber


def readKeyFile() -> Type[Account]:
    def detable():
        s1 = string.ascii_letters + string.digits
        s2 = string.digits + string.ascii_letters
        return str.maketrans(dict(zip(s2, s1)))
    file = open('.\\key.coolapk', 'r')
    content = file.read().translate(detable())
    l = content.split("LoginForCoolapk")
    r = []
    if len(l) != 3:
        raise LoginError(LoginErrorAttributes.KEYFILE_ERROR.value)
    for i in l:
        r.append(base64.b64decode(i.encode()).decode())
    account = Account
    account.uid = r[0]
    account.username = r[1]
    account.token = r[2]
    return account


def writeKeyFile(account: Type[Account]):
    def entable():
        s1 = string.ascii_letters + string.digits
        s2 = string.digits + string.ascii_letters
        return str.maketrans(dict(zip(s1, s2)))
    file = open('.\\key.coolapk', 'w')
    writecontent = ("%sLoginForCoolapk%sLoginForCoolapk%s" %
                    (base64.b64encode(str(account.uid).encode()).decode(),
                     base64.b64encode(account.username.encode()).decode(),
                     base64.b64encode(
                         account.token.encode()).decode())).translate(entable())
    file.write(writecontent)
