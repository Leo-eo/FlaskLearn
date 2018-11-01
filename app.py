from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request  # 获取参数
import config
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


def create_result(code, msg):
    result = {
        "code": code,
        'msg': msg
    }
    return jsonify(result)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(16), nullable=False)


@app.route('/')
def index():
    context = {
        "username": "李俊",
        "age": 24
    }
    return render_template("index.html", **context)


@app.route('/register', methods=['get', 'post'])
def register():
    username = request.values.get('username')  # 获取参数
    password = request.values.get('password')

    if username and password:
        result = User.query.filter(User.username == username).first()
        if not result:
            # 增加
            user = User(username=username, password=password)
            db.session.add(user)
            # 事务
            db.session.commit()
        else:
            return create_result(2, '该用户名已存在')
    else:
        return create_result(0, '用户名或密码不能为空')
    # "注册成功"
    return create_result(1, '注册成功')


@app.route('/login', methods=['get', 'post'])
def login():
    username = request.values.get('username')  # 获取参数
    pwd = request.values.get('password')

    if username and pwd:
        result = User.query.filter(User.username == username).first()
        if not result:
            return create_result(404, '该用户名不存在')
        else:
            if result.password == pwd:
                return create_result(1, '登录成功')
            else:
                return create_result(0, '密码错误')
    else:
        return create_result(0, '用户名或密码不能为空')


db.create_all()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug='True')
