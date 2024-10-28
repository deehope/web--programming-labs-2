from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=["POST"])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div-form.html', error='Оба поля должны быть заполнены')

    try:
        x1 = int(x1)
        x2 = int(x2)
        if x2 == 0:
            return render_template('lab4/div-form.html', error='Деление на ноль невозможно', x1=x1, x2=x2)
        result = x1 / x2
        return render_template('lab4/div-form.html', x1=x1, x2=x2, result=result)

    except ValueError:
        return render_template('lab4/div-form.html', error='Оба поля должны содержать числа')
    

@lab4.route('/lab4/add-form')
def add_form():
    return render_template('lab4/add-form.html')


@lab4.route('/lab4/add', methods=["POST"])
def add():
    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/add-form.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=["POST"])
def mul():
    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mul-form.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=["POST"])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/sub-form.html', error='Оба поля должны быть заполнены')

    try:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
        return render_template('lab4/sub-form.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/sub-form.html', error='Оба поля должны содержать числа')


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=["POST"])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/pow-form.html', error='Оба поля должны быть заполнены')

    try:
        x1 = int(x1)
        x2 = int(x2)

        if x1 == 0 and x2 == 0:
            return render_template('lab4/pow-form.html', error='0 в степени 0 не определено')

        result = x1 ** x2
        return render_template('lab4/pow-form.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/pow-form.html', error='Оба поля должны содержать числа')
    

tree_count = 0
MAX_TREES = 10  

@lab4.route('/lab4/tree', methods=["GET", "POST"])
def tree():
    global tree_count

    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < MAX_TREES:
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Alex Ivanov', 'gender': 'M'},
    {'login': 'bob', 'password': '555', 'name': 'Bob Marley', 'gender': 'M'},
    {'login': 'max', 'password': '111', 'name': 'Max Planck', 'gender': 'M'},
    {'login': 'nod', 'password': '321', 'name': 'Nod Green', 'gender': 'F'}
]

@lab4.route("/lab4/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            login = session['login']
            user = next((user for user in users if user['login'] == login), None)
            if user:
                return render_template("lab4/login.html", authorized=True, name=user['name'])
        return render_template("lab4/login.html", authorized=False)

    login = request.form.get('login')
    password = request.form.get('password')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login 
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route("/lab4/fridge", methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template("lab4/fridge.html", message="", snowflakes=0)

    temperature = request.form.get('temperature')
    if not temperature:
        message = "Ошибка: не задана температура"
        return render_template("lab4/fridge.html", message=message, snowflakes=0)

    try:
        temperature = int(temperature)
    except ValueError:
        message = "Ошибка: некорректное значение температуры"
        return render_template("lab4/fridge.html", message=message, snowflakes=0)

    if temperature < -12:
        message = "Не удалось установить температуру — слишком низкое значение"
        snowflakes = 0
    elif temperature > -1:
        message = "Не удалось установить температуру — слишком высокое значение"
        snowflakes = 0
    elif -12 <= temperature <= -9:
        message = f"Установлена температура: {temperature}°С"
        snowflakes = 3
    elif -8 <= temperature <= -5:
        message = f"Установлена температура: {temperature}°С"
        snowflakes = 2
    elif -4 <= temperature <= -1:
        message = f"Установлена температура: {temperature}°С"
        snowflakes = 1
    else:
        message = "Ошибка: некорректное значение температуры"
        snowflakes = 0

    return render_template("lab4/fridge.html", message=message, snowflakes=snowflakes)


grain_prices = {
    "ячмень": 12345,
    "овёс": 8522,
    "пшеница": 8722,
    "рожь": 14111
}

@lab4.route("/lab4/grain_order", methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template("lab4/grain_order.html", message="")
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')

    if not weight:
        message = "Ошибка: вес не был указан"
        return render_template("lab4/grain_order.html", message=message)
    try:
        weight = float(weight)
    except ValueError:
        message = "Ошибка: некорректное значение веса"
        return render_template("lab4/grain_order.html", message=message)
    
    if weight <= 0:
        message = "Ошибка: вес должен быть положительным числом"
        return render_template("lab4/grain_order.html", message=message)
    
    if weight > 500:
        message = "Ошибка: такого объёма сейчас нет в наличии"
        return render_template("lab4/grain_order.html", message=message)
    
    price_per_ton = grain_prices.get(grain_type)
    total_price = weight * price_per_ton
    discount_message = ""

    if weight > 50:
        discount = total_price * 0.10
        total_price -= discount
        discount_message = f"Применена скидка за большой объём: 10% (скидка {discount:.2f} руб)."
        
    message = (f"Заказ успешно сформирован. Вы заказали {grain_type}. "
               f"Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб. {discount_message}")
    return render_template("lab4/grain_order.html", message=message)


@lab4.route("/lab4/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("lab4/register.html", error="")

    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    gender = request.form.get('gender')

    if not login or not password or not name or not gender:
        error = "Все поля обязательны для заполнения."
        return render_template("lab4/register.html", error=error)

    if any(user['login'] == login for user in users):
        error = "Пользователь с таким логином уже существует."
        return render_template("lab4/register.html", error=error)

    users.append({'login': login, 'password': password, 'name': name, 'gender': gender})

    session['login'] = login
    return redirect('/lab4/login')


@lab4.route("/lab4/users", methods=['GET'])
def user_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']
    return render_template("lab4/users.html", users=users, current_login=current_login)


@lab4.route("/lab4/delete_user", methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    login_to_delete = request.form.get('login')

    if session['login'] == login_to_delete:
        global users
        users = [user for user in users if user['login'] != login_to_delete]
        session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route("/lab4/edit_user", methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        for user in users:
            if user['login'] == login:
                user['name'] = new_name if new_name else user['name']
                user['password'] = new_password if new_password else user['password']
                break

        return redirect('/lab4/users')

    user_data = next((user for user in users if user['login'] == login), None)
    return render_template("lab4/edit_user.html", user=user_data)