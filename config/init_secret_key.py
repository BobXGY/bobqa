from os import urandom

# 生成一个盐并写入文件key
key = urandom(24)

with open('config/key', 'wb') as f:
    f.write(key)
