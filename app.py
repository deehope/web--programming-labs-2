from flask import Flask, redirect
import os
from dotenv import load_dotenv
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

load_dotenv('/.env')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ключ')
app.config['DB-TYPE'] = os.getenv('DB-TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
        </ul>


        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""