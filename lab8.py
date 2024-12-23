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

    # Автоматический логин
    login_user(new_user)

    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'  # True, если галка установлена

    # Проверка на пустые значения
    if not login_form or login_form.strip() == "":
        return render_template('lab8/login.html', error='Логин не должен быть пустым')

    if not password_form or password_form.strip() == "":
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    # Проверка существования пользователя
    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        # Если галочка "Запомнить меня" установлена, передаем remember=True
        login_user(user, remember=remember_me)
        return redirect('/lab8/')

    # Если пользователь не найден или пароль неверен
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'  # True, если чекбокс выбран
    is_public = request.form.get('is_public') == 'on'  # True, если чекбокс выбран

    # Проверка на пустые поля
    if not title or not title.strip():
        return render_template('lab8/create.html', error='Заголовок не может быть пустым')
    if not article_text or not article_text.strip():
        return render_template('lab8/create.html', error='Текст статьи не может быть пустым')

    # Создаем новую статью
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0  # По умолчанию 0 лайков
    )
    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles')


@lab8.route('/lab8/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    # Получаем статью по ID
    article = articles.query.get_or_404(article_id)

    # Проверка, что статья принадлежит текущему пользователю
    if article.login_id != current_user.id:
        return redirect('/lab8/')

    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = request.form.get('is_favorite') == 'on'  # True, если чекбокс выбран
        is_public = request.form.get('is_public') == 'on'  # True, если чекбокс выбран

        # Проверка на пустые поля
        if not title or not title.strip():
            return render_template('lab8/edit.html', article=article, error='Заголовок не может быть пустым')
        if not article_text or not article_text.strip():
            return render_template('lab8/edit.html', article=article, error='Текст статьи не может быть пустым')

        # Обновляем статью
        article.title = title
        article.article_text = article_text
        article.is_favorite = is_favorite
        article.is_public = is_public

        # Сохраняем изменения в базе данных
        db.session.commit()

        return redirect('/lab8/articles')

    return render_template('lab8/edit.html', article=article)


@lab8.route('/lab8/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    # Получаем статью по ID
    article = articles.query.get_or_404(article_id)

    # Проверка, что статья принадлежит текущему пользователю
    if article.login_id != current_user.id:
        return redirect('/lab8/')

    # Удаляем статью из базы данных
    db.session.delete(article)
    db.session.commit()

    return redirect('/lab8/articles')