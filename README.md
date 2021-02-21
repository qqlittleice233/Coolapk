# Coolapk
A python module for Coolapk.

## Functions:
1. Login Coolapk by Python
2. coming soon

## Use:
```python
from Coolapk import function
from urllib import parse

coolapk = function.Login('Your Account', 'Your Password')
account = coolapk.get() # Return an Account object
print(account.uid)
print(parse.unquote(account.username))
print(account.token)
```
