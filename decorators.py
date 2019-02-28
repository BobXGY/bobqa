from functools import wraps
from flask import url_for, redirect, session


# 登陆限制装饰器
# 用于需要登陆的页面，如果没有登陆则要求登陆(跳转至登陆页面)
def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wapper
