from flask import Flask, redirect
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

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
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>

        <ul>
            <li><a href = "/lab1">Первая лабораторная</a></li>
            <li><a href = "/lab2">Вторая лабораторная</a></li>
            <li><a href = "/lab3">Третья лабораторная</a></li>
        </ul>


        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""