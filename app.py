from flask import Flask, render_template, request, session, redirect, url_for
from config import config
from models import User, Question, Answer
from extends import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def main():
    return redirect(url_for('index'))


@app.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        context = {
            # 按create_time字段排序，若要逆序，只需在字符串前加上'-'
            'questions': Question.query.order_by('-create_time').all()
        }
    elif request.method == 'POST':
        search_key = request.form.get('key')
        context = {
            # 按create_time字段排序，若要逆序，只需在字符串前加上'-'
            'questions': Question.query.filter(Question.title.ilike('%' + search_key + '%')).order_by(
                '-create_time').all()
        }

    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登陆
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            if request.form.get('hold') == 'on':
                session.permanent = True
            return redirect(url_for('index'))
        else:
            return '用户不存在或者密码错误'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    """
    注册
    :return:
    """
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password_repeat = request.form.get('password-repeat')

        user = User.query.filter(User.telephone == telephone).first()

        # 手机号码验证，不能重复注册
        if password != password_repeat:
            return '两次输入密码不相同'
        elif user:
            return '该手机号已经被注册，请更换手机号'
        # 两次密码验证

        # 通过前两次验证之后即可将数据添加进数据库，完成注册
        user = User(telephone=telephone, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    """
    GET请求则返回发帖页面
    POST则是创建帖子
    :return:
    """
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question_ = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question_.author = user
        db.session.add(question_)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    """
    注销登陆
    :return:
    """
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/detail/<question_id>')
def detail(question_id):
    """
    帖子详情
    :param question_id: 帖子id
    :return:
    """
    question_ = Question.query.filter(Question.id == question_id).first()
    owner = None
    current_user_id = session.get('user_id')
    article_author_id = question_.author_id
    if current_user_id == article_author_id:
        owner = True

    return render_template('detail.html', question=question_, question_id=question_id, owner=owner)


@app.route('/delete/<question_id>')
def delete_item(question_id):
    """
    删除帖子, 先删除所有回复，再删除帖子
    :return:
    """
    question_ = Question.query.filter(Question.id == question_id).first()

    current_user_id = session.get('user_id')
    article_author_id = question_.author_id

    if article_author_id == current_user_id:
        answers = Answer.query.filter(Answer.question_id == question_id).all()
        for each_answer in answers:
            db.session.delete(each_answer)
        db.session.delete(question_)
        db.session.commit()
        return "删除成功，点击返回<a href=\"" + url_for('index') + "\">主页</a>"
    else:
        return "未获授权"


@app.route('/my_info/')
@login_required
def my_info():
    return render_template('my_info.html')


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    """
    给帖子添加回复
    :return:
    """
    content = request.form.get('answer-content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question_ = Question.query.filter(Question.id == question_id).first()
    answer.question = question_
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


# 上下文处理器装饰器
# 可以让变量在所有html模板中可见
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    else:
        # 钩子函数必须返回一个字典，即使是空的
        return {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
