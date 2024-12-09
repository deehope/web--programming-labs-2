from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, flash
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from dotenv import load_dotenv

test = Blueprint('test', __name__)

load_dotenv()


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


@test.route('/test/')
def messenger_home():
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    login = session['login']
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login FROM users WHERE login != %s;", (login,))
    else:
        cur.execute("SELECT id, login FROM users WHERE login != ?;", (login,))

    users = cur.fetchall()

    if current_app.config['DB_TYPE'] == 'sqlite':
        users = [dict(user) for user in users]

    db_close(conn, cur)
    return render_template('test/home.html', login=login, users=users)


@test.route('/test/chat/<int:receiver_id>', methods=['GET', 'POST'])
def chat(receiver_id):
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    login = session['login']
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login FROM users WHERE id = %s;", (receiver_id,))
    else:
        cur.execute("SELECT id, login FROM users WHERE id = ?;", (receiver_id,))

    receiver = cur.fetchone()
    if not receiver:
        db_close(conn, cur)
        return redirect(url_for('test.messenger_home'))

    if request.method == 'POST':
        message_text = request.form.get('message')
        if message_text:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    INSERT INTO messages (sender_id, receiver_id, message_text)
                    VALUES ((SELECT id FROM users WHERE login = %s), %s, %s);
                """, (login, receiver_id, message_text))
            else:
                cur.execute("""
                    INSERT INTO messages (sender_id, receiver_id, message_text)
                    VALUES ((SELECT id FROM users WHERE login = ?), ?, ?);
                """, (login, receiver_id, message_text))
            db_close(conn, cur)
            return redirect(url_for('test.chat', receiver_id=receiver_id))

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT m.message_text, u.login, m.timestamp, m.id 
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE (m.sender_id = (SELECT id FROM users WHERE login = %s) AND m.receiver_id = %s)
               OR (m.sender_id = %s AND m.receiver_id = (SELECT id FROM users WHERE login = %s))
            ORDER BY m.timestamp;
        """, (login, receiver_id, receiver_id, login))
    else:
        cur.execute("""
            SELECT m.message_text, u.login, m.timestamp, m.id 
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE (m.sender_id = (SELECT id FROM users WHERE login = ?) AND m.receiver_id = ?)
               OR (m.sender_id = ? AND m.receiver_id = (SELECT id FROM users WHERE login = ?))
            ORDER BY m.timestamp;
        """, (login, receiver_id, receiver_id, login))

    messages = cur.fetchall()

    if current_app.config['DB_TYPE'] == 'sqlite':
        messages = [dict(message) for message in messages]

    db_close(conn, cur)
    return render_template('test/chat.html', login=login, receiver=receiver, messages=messages)


@test.route('/test/delete_message/<int:message_id>/<int:receiver_id>')
def delete_message(message_id, receiver_id):
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    login = session['login']
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))

    user_id = cur.fetchone()
    if not user_id:
        db_close(conn, cur)
        return redirect(url_for('test.messenger_home'))

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT * FROM messages WHERE id = %s AND (sender_id = %s OR receiver_id = %s);
        """, (message_id, user_id['id'], user_id['id']))
    else:
        cur.execute("""
            SELECT * FROM messages WHERE id = ? AND (sender_id = ? OR receiver_id = ?);
        """, (message_id, user_id['id'], user_id['id']))
    message = cur.fetchone()

    if message:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM messages WHERE id = %s;", (message_id,))
        else:
            cur.execute("DELETE FROM messages WHERE id = ?;", (message_id,))
    
    db_close(conn, cur)
    flash('Сообщение успешно удалено.', 'success')
    return redirect(url_for('test.chat', receiver_id=receiver_id))


@test.route('/test/admin/', methods=['GET', 'POST'])
def admin():
    if 'login' not in session or session['login'] != 'admin':
        return redirect(url_for('lab5.login'))    
    conn, cur = db_connect()
    error = None
    if request.method == 'POST':
        if 'delete_user' in request.form:
            user_id = request.form.get('user_id')
            if user_id:
                try:
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("DELETE FROM articles WHERE user_id = %s;", (user_id,))
                    else:
                        cur.execute("DELETE FROM articles WHERE user_id = ?;", (user_id,))
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("DELETE FROM messages WHERE sender_id = %s OR receiver_id = %s;", (user_id, user_id))
                    else:
                        cur.execute("DELETE FROM messages WHERE sender_id = ? OR receiver_id = ?;", (user_id, user_id))
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
                    else:
                        cur.execute("DELETE FROM users WHERE id = ?;", (user_id,))
                    flash('Пользователь и все связанные данные были успешно удалены.', 'success')
                except Exception as e:
                    error = f"Произошла ошибка при удалении пользователя: {str(e)}"
                    conn.rollback()  # Отменяем все изменения, если произошла ошибка
            else:
                error = "Пользователь не выбран для удаления."

        elif 'edit_user' in request.form:
            user_id = request.form.get('edit_user_id')
            new_login = request.form.get('new_login')
            if user_id and new_login:
                try:
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("UPDATE users SET login = %s WHERE id = %s;", (new_login, user_id))
                    else:
                        cur.execute("UPDATE users SET login = ? WHERE id = ?;", (new_login, user_id))
                    flash('Логин пользователя был успешно обновлен.', 'success')
                except Exception as e:
                    error = f"Произошла ошибка при обновлении логина: {str(e)}"
                    conn.rollback()  # Отменяем все изменения, если произошла ошибка
            else:
                error = "Не все поля заполнены."
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login FROM users;")
    else:
        cur.execute("SELECT id, login FROM users;")
    users = cur.fetchall()
    if current_app.config['DB_TYPE'] == 'sqlite':
        users = [dict(user) for user in users]
    db_close(conn, cur)
    return render_template('test/admin.html', users=users, error=error)
