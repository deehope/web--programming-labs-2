from flask import Flask, redirect
import os
from os import path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from test import test

app = Flask(__name__)
load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'key')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.config['SESSION_COOKIE_NAME'] = 'lab8_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Используйте True, если используете HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_PERMANENT'] = True  # Сессия будет постоянной, если галочка "Запомнить меня" установлена
app.config['SESSION_TYPE'] = 'filesystem'  # Это может помочь избежать проблем с кодировкой

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'sokolova_darya_orm'
    db_user = 'sokolova_darya_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "sokolova_darya_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(test)

@app.route("/")
def start():
    return redirect("/menu", code=302)


@app.route("/menu")
def menu():
    return """
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>НГТУ, Лабораторные работы</title>
        <style>
            footer {
                background-color: rgb(255, 195, 195);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 12px;
                padding: 10px;
                margin: 0px;
                text-align: right;
                font-style: italic;
                position: fixed;
                bottom: 0;
                right: 0;
                left: 0;
            }
            header {
                background-color: rgb(255, 195, 195);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                padding: 10px; 
                margin: 0;
                font-style: italic;
                width: 100%;
            }
            body {
                background-color: rgb(248, 248, 248);
                margin: 0; 
                padding: 0; 
            }
        </style>  
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <ul>
            <li><a href = "/lab1">Первая лабораторная</a></li>
            <li><a href = "/lab2">Вторая лабораторная</a></li>
            <li><a href = "/lab3">Третья лабораторная</a></li>
            <li><a href = "/lab4">Четвертая лабораторная</a></li>
            <li><a href = "/lab5">Пятая лабораторная</a></li>
            <li><a href = "/lab6">Шестая лабораторная</a></li>
            <li><a href = "/lab7">Седьмая лабораторная</a></li>
            <li><a href = "/lab8">Восьмая лабораторная</a></li>
            <li><a href = "/test">РГЗ</a></li>
        </ul>


        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""