from pydantic.main import BaseModel


class Account(BaseModel):
    uid: int
    username: str
    token: str


class User(BaseModel):
    uid: int
    username: str
    admintype: int
    level: int  # 等级
    experience: int  # 经验
    next_level_experience: int  # 升下一级所需经验
    next_level_percentage: float  # 经验百分比 (距离下一级)
    verify_title: str  # 认证标题
    verify_status: int  # 认证状态
    feed: int  # 动态数
    follow: int  # 他/她关注的数量
    fans: int  # 他/她的粉丝数
