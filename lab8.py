from flask import Blueprint, session, render_template, request, redirect
from db import db
from flask_login import login_user, login_required, current_user, logout_user
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login=current_user.login if current_user.is_authenticated else 'anonymous')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверка на пустое имя пользователя
    if not login_form or login_form.strip() == "":
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    
    # Проверка на пустой пароль
    if not password_form or password_form.strip() == "":
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')
    
    # Проверка, существует ли пользователь с таким именем
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    # Хеширование пароля и сохранение пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые значения
    if not login_form or login_form.strip() == "":
        return render_template('lab8/login.html', error='Логин не должен быть пустым')
    
    if not password_form or password_form.strip() == "":
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    # Проверка существования пользователя
    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember = False)
        return redirect('/lab8/')

    # Если пользователь не найден или пароль неверен
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles')
@login_required
def article_list():
    return "список статей"


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')
