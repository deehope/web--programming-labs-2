from flask import Blueprint, render_template, request, session, current_app, jsonify, abort
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from dotenv import load_dotenv

lab7 = Blueprint('lab7', __name__)

load_dotenv()

# Функции для работы с базой данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='darya_sokolova_knowledge_base',
            user='darya_sokolova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else: 
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path)) 
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def main():
    login = session.get('login', '')  # Получаем логин из сессии
    return render_template('/lab7/index.html', login=login)


# Маршрут для работы с фильмами
@lab7.route('/lab7/rest-api/films/', methods=['GET', 'POST'])
def films():
    conn, cur = db_connect()

    if request.method == 'GET':  # Получение списка фильмов
        cur.execute("SELECT * FROM films;")
        films = cur.fetchall()
        if current_app.config['DB_TYPE'] == 'sqlite':
            films = [dict(film) for film in films]
        db_close(conn, cur)
        return jsonify(films)
    
    elif request.method == 'POST':  # Добавление нового фильма
        data = request.get_json()
        title = data.get('title')
        title_ru = data['title_ru']
        year = data['year']
        description = data['description']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id;",
                (title, title_ru, year, description)
            )
            film_id = cur.fetchone()['id']
        else:
            cur.execute(
                "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?);",
                (title, title_ru, year, description)
            )
            film_id = cur.lastrowid
        
        db_close(conn, cur)
        return jsonify({'id': film_id}), 201


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def film_details(id):
    conn, cur = db_connect()

    if request.method == 'GET':  # Получение фильма по ID
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
        
        film = cur.fetchone()
        if not film:
            db_close(conn, cur)
            abort(404)

        if current_app.config['DB_TYPE'] == 'sqlite':
            film = dict(film)

        db_close(conn, cur)
        return jsonify(film)
    
    elif request.method == 'PUT':  # Обновление фильма
        data = request.get_json()
        title = data.get('title')
        title_ru = data['title_ru']
        year = data['year']
        description = data['description']

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s;",
                (title, title_ru, year, description, id)
            )
        else:
            cur.execute(
                "UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?;",
                (title, title_ru, year, description, id)
            )
        
        db_close(conn, cur)
        return jsonify({'status': 'updated'})

    elif request.method == 'DELETE':  # Удаление фильма
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("DELETE FROM films WHERE id = ?;", (id,))
        
        db_close(conn, cur)
        return jsonify({'status': 'deleted'})


