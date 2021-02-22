from pydantic import BaseModel
from enum import Enum


class Error(Exception):
    """Base class for exceptions in this module."""


class LoginErrorAttributes(Enum):
    SESSID_NOT_FOUND = "获取SESSID失败"
    FORWARD_NOT_FOUND = "获取forward失败"
    KEYFILE_ERROR = "Key文件错误，请删除并重新登录"
    REQHASH_NOT_FOUND = "获取ReqHash失败"


class GetDataErrorAttributes(Enum):
    KEY_ERROR = "用户可能被封禁，或无该用户"


class LoginError(Error):
    def __init__(self, message):
        self.message = message


class GetDataError(Error):
    def __init__(self, message):
        self.message = message
