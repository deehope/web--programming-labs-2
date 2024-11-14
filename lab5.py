from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv

lab5 = Blueprint('lab5', __name__)

load_dotenv()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login = session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='darya_sokolova_knowledge_base',
            user='darya_sokolova_knowledge_base',
            password='123'      
        )
        cur = conn.cursor(cursor_factory= RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        error = 'Заполните оба поля' if not login and not password else (
            'Заполните логин' if not login else 'Заполните пароль'
        )
        return render_template('lab5/register.html', error=error)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    db_close(conn, cur)

    return render_template('lab5/success.html', login=login) 


@lab5.route('/lab5/success')
def success():
    login = request.args.get('login')
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        error = 'Заполните оба поля' if not login and not password else (
            'Заполните логин' if not login else 'Заполните пароль'
        )
        return render_template('lab5/login.html', error=error)
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash (user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login = login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        error = 'Заполните оба поля' if not title and not article_text else (
            'Заполните тему статьи' if not title else 'Заполните текст статьи'
        )
        return render_template('lab5/create_article.html', error=error)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", 
                (user_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);", 
                (user_id, title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s;", (user_id, ))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=?;", (user_id, ))
    articles = cur.fetchall()

    if not articles:
        no_articles_message = 'У вас пока нет ни одной статьи'
        return render_template('lab5/articles.html', no_articles_message=no_articles_message)

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/login')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="Статья не найдена.")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if article['user_id'] != user['id']:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="У вас нет доступа для редактирования этой статьи.")

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            error = 'Заполните все поля для сохранения изменений.'
            return render_template('lab5/edit_article.html', article=article, error=error)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", 
                        (title, article_text, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", 
                        (title, article_text, article_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="Статья не найдена.")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if article['user_id'] != user['id']:
        db_close(conn, cur)
        return render_template('lab5/error.html', error="У вас нет прав для удаления этой статьи.")
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

