from os import system

# DEBUG = True

'''使用文件key中的内容作为盐，若不存在则创建文件'''
try:
    f = open('config/key', 'rb')
    f.close()
except FileNotFoundError:
    system('python config/init_secret_key.py')

'''key长度检查'''
key_stat = False
with open('config/key', 'rb') as f:
    if len(f.readline()) == 24:
        key_stat = True
    else:
        key_stat = False

if key_stat:
    pass
else:
    system('python config/init_secret_key.py')

with open('config/key', 'rb') as f:
    key = f.readline()

SECRET_KEY = key
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:3699@127.0.0.1/bobqa?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
