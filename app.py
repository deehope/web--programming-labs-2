from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route('/lab2/example')
def example():
    name = 'Соколова Дарья'
    number = 'Лабораторная работа 2'
    course = '3 курс'
    group = 'ФБИ-23'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name':'апельсины', 'price':80},
        {'name':'манадарины', 'price': 95},
        {'name':'манго', 'price': 320}
    ]
    books = [
        {'author': 'Донна Тартт', 'name': 'Щегол', 'genre': 'роман', 'count': 828 },
        {'author': 'Мария Метлицкая', 'name': 'Дом в Мансуровском', 'genre': 'роман', 'count': 340 },
        {'author': 'Сергей Лукьяненко', 'name': 'Форсайт', 'genre': 'фантастика', 'count': 271 },
        {'author': 'Ребекка Яррос', 'name': 'Железное пламя', 'genre': 'фэнтези', 'count': 953 },
        {'author': 'Татьяна Корсакова', 'name': 'Марь', 'genre': 'мистика', 'count': 350 },
        {'author': 'Роберт Чалдини', 'name': 'Психология влияния. 7-е расширенное издание', 'genre': 'детектив', 'count': 191 },
        {'author': 'Дарья Донцова', 'name': 'Блоха на балу', 'genre': 'роман', 'count': 828 },
        {'author': 'Мери Ли', 'name': 'Квента. Трилогия', 'genre': 'роман', 'count': 630 },
        {'author': 'Дэвид Эллис', 'name': 'Дом лжи', 'genre': 'детектив', 'count': 426 },
        {'author': 'Наталья Мамлеева', 'name': 'Злодейка своего романа', 'genre': 'фэнтези', 'count': 220 }
    ]
    return render_template('example.html', number = number, name = name, group = group, course = course, fruits = fruits, books = books)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/berries')
def berries():
    return render_template('berries.html')