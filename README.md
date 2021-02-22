# Coolapk
A python module for Coolapk.

## Functions:
- [✓] Login Coolapk by Python
- [✓] Get UserData

### TODO:
1. Send Message
2. Get Feed Information

## Use:
### Login:
```python
from Coolapk.application import CoolapkApplication
from urllib import parse

account = CoolapkApplication.login('Your Account', 'Your Password')
print(account.uid)
print(parse.unquote(account.username))
print(account.token)
```
### GetUserData:
```python
from Coolapk.application import CoolapkApplication

user = CoolapkApplication.getUserData(10002)
print(user.uid)
print(user.username)
print(user.admintype)
print(user.level)
print(user.experience)
print(user.next_level_experience)
print(user.next_level_percentage)
print(user.verify_title)
print(user.verify_status)
print(user.feed)
print(user.follow)
print(user.fans)
```
