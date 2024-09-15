from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/index")
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
        </ul>


        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""
@app.route("/lab1")
def lab1():
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

        <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        
        <a href="/menu">меню</a>

        <h2>Реализованные роуты</h2>

        <ul>
            <li><a href = "/lab1/oak">/lab1/oak - Дуб</a></li>
            <li><a href = "/lab1/student">/lab1/student - Студент</a></li>
            <li><a href = "/lab1/python">/lab1/python - Python</a></li>
            <li><a href = "/lab1/flower">/lab1/flower - Роза</a></li>
        </ul>

        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""
@app.route("/lab1/oak")
def oak():
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>

    <body>
        <h1>Дуб</h1>
        <img src="''' + url_for('static', filename='oak.webp') + '''">
    </body>
</html>
'''
@app.route("/lab1/student")
def student():
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Соколова Дарья Антоновна, лабораторная 1</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>

        <h1>Соколова Дарья Антоновна</h1>
        <img src="''' + url_for('static', filename='logo.png') + '''">

        <footer>
            &copy; Соколова Дарья, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
    '''

@app.route("/lab1/python")
def puthon():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Соколова Дарья Антоновна, лабораторная 1</title>
            <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
            <style>
                h1 {
                    text-align: center;
                }
                p {
                    font-size: 28px;
                    text-align: justify; 
                }
                .image{
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <header>
                НГТУ, ФБ, Лабораторная работа 1
            </header>

            <h1>Язык python</h1>

            <p>Python является мультипарадигменным языком программирования, поддерживающим императивное, процедурное, 
            структурное, объектно-ориентированное программирование, метапрограммирование, функциональное программирование и асинхронное
            программирование. Задачи обобщённого программирования решаются за счёт динамической типизации. Аспектно-ориентированное 
            программирование частично поддерживается через декораторы, более полноценная поддержка обеспечивается дополнительными 
            фреймворками. </p>
            <p>Такие методики как контрактное и логическое программирование можно реализовать с помощью библиотек или расширений.
            Основные архитектурные черты — динамическая типизация, автоматическое управление памятью, полная интроспекция, механизм обработки
            исключений, поддержка многопоточных вычислений с глобальной блокировкой интерпретатора (GIL), высокоуровневые структуры данных. 
            Поддерживается разбиение программ на модули, которые, в свою очередь, могут объединяться в пакеты.</p>
            
            <div class='image'>
                <img src="''' + url_for('static', filename='python.png') + '''">
            </div>
        </body>
    </html>
    '''

@app.route("/lab1/flower")
def flower():
    return '''
    <!DOCTYPE html>
    <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Соколова Дарья Антоновна, лабораторная 1</title>
            <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') + '''">
            <style>
                h1 {
                    text-align: center;
                }
                p {
                    font-size: 28px;
                    text-align: justify; 
                }
                .image{
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <h1>Роза</h1>

            <p>Роза — собирательное название видов и сортов представителей рода Шипо́вник (лат. Rósa), выращиваемых человеком и растущих 
            в дикой природе. Бо́льшая часть сортов роз получена в результате длительной селекции путём многократных повторных скрещиваний 
            и отбора. Некоторые сорта являются формами дикорастущих видов. </p>
            <p>Розы впервые начали выращивать в Древнем Риме, хотя основное назначение садов того времени было выращивание полезных 
            растений (плодовых, овощных, пряных и лекарственных), но в произведениях древнеримских писателей встречается описание около 
            10 сортов роз. Геродот уже в V веке до н. э. в своей «Истории» описывает сады царя Мидаса в Македонии и упоминает там 
            махровую розу. Теофраст в 300 году до н. э. описывает сады Греции и даёт описание роз с 15, 20 и даже 100 лепестками. На 
            великолепной мозаике из Помпеи, хранящейся в Неаполитанском музее, можно увидеть и дамасскую розу (Rosa damascena), родиной 
            которой несомненно является восток, и уже оттуда она попала в сады Южной Италии. С распадом Римской Империи садоводство перешло 
            в монастыри. Именно монастырские сады послужили прототипом садов по ту сторону Альп. Карл Великий в своей инструкции по 
            управлению поместьями Capitulare de villis указал перечень растений, которые необходимо выращивать, среди которых были и розы. 
            Во времена Каролингов в садах декоративные растения выращивались прежде всего с лекарственной целью, хотя, несомненно, обращалось 
            внимание и на их красоту.</p>
            
            <div class='image'>
                <img src="''' + url_for('static', filename='rosa.jpeg') + '''">
            </div>
        </body>
    </html>
    '''