from flask import Flask
app = Flask(__name__)

@app.route("/")
def start():
    return """
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Соколова Дарья Антоновна, лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""
