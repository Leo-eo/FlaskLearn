from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import config

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
        "age": 23
    }
    return render_template("index.html", **context)


@app.route('/register&username=<username>&password=<pwd>')
def register(username, pwd):
    # 增加
    user = User(username=username, password=pwd)
    db.session.add(user)
    # 事务
    db.session.commit()

    # "注册成功"
    return create_result(1, '注册成功')


# app.route('/login?<username>&<pwd>')
# ef login(username, pwd):
#   result = User.query.filter(User.username == username, User.password = pwd).first()
#
#   if result is None:
#       return {"code": 0, "msg": "登录失败"}
#   else:
#       return {"code": 0, "msg": "登录成功"}


db.create_all()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
