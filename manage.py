from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from extends import db
from models import User, Question, Answer

manager = Manager(app)

# 绑定数据库
migrate = Migrate(app, db)

# 将迁移脚本命令添加到manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
