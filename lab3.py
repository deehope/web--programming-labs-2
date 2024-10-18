from flask import Blueprint, render_template, request, make_response, redirect, url_for
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'аноним'
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age') or 'неизвестный'
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age = age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name')
    resp.set_cookie('age')
    resp.set_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
        
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')

    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    backgroundcolor = request.args.get('background-color')
    fontsize = request.args.get('fontsize')
    fontweight = request.args.get('fontweight')
    
    resp = make_response(redirect('/lab3/settings'))

    if color:
        resp.set_cookie('color', color)
    
    if backgroundcolor:
        resp.set_cookie('background-color', backgroundcolor)
    
    if fontsize:
        resp.set_cookie('fontsize', fontsize)

    if fontweight:
        resp.set_cookie('fontweight', fontweight)

    if not (color or backgroundcolor or fontsize or fontweight):
        color = request.cookies.get('color')
        backgroundcolor = request.cookies.get('background-color')
        fontsize = request.cookies.get('fontsize')
        fontweight = request.cookies.get('fontweight')
        resp = make_response(render_template('lab3/settings.html', 
                                             color=color, 
                                             backgroundcolor=backgroundcolor, 
                                             fontsize=fontsize,
                                             fontweight=fontweight))
    
    return resp


@lab3.route('/lab3/form2')
def form2():
    errors = {}

    form_submitted = bool(request.args)
    
    pass_name = request.args.get('pass_name', '')
    if form_submitted and not pass_name:
        errors['pass_name'] = 'Заполните поле!'

    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'

    age = request.args.get('age')
    if form_submitted:
        if not age or age == '':
            errors['age'] = 'Заполните поле!'
        else:
            try:
                age = int(age)
                if age < 1 or age > 120:
                    errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
            except ValueError:
                errors['age'] = 'Некорректный возраст!'

    departure = request.args.get('departure', '')
    if form_submitted and not departure:
        errors['departure'] = 'Заполните поле!'

    destination = request.args.get('destination', '')
    if form_submitted and not destination:
        errors['destination'] = 'Заполните поле!'

    date = request.args.get('date', '')
    if form_submitted and not date:
        errors['date'] = 'Заполните поле!'

    insurance = request.args.get('insurance') == 'on'

    if 'age' in errors:
        price = 0
        ticket_type = ''
    else:
        if age and age >= 18:
            base_price = 1000
            ticket_type = 'Взрослый'
        else:
            base_price = 700
            ticket_type = 'Детский'

        if shelf in ['lower', 'lower_side']:
            base_price += 100
        if bedding:
            base_price += 75
        if luggage:
            base_price += 250
        if insurance:
            base_price += 150

        price = base_price

    return render_template('lab3/form2.html', errors=errors, pass_name=pass_name, shelf=shelf,
                           bedding=bedding, luggage=luggage, age=age, departure=departure,
                           destination=destination, date=date, insurance=insurance,
                           ticket_type=ticket_type, price=price)


@lab3.route('/lab3/settings/del_cookie_2')
def del_cookie_2():
    resp = make_response(redirect(url_for('lab3.settings')))
    resp.delete_cookie('color')
    resp.delete_cookie('background-color')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('fontweight')

    return resp


cars = [
    {"name": "Toyota Corolla", "price": 15000, "brand": "Toyota", "year": 2019},
    {"name": "Ford Mustang", "price": 30000, "brand": "Ford", "year": 2020},
    {"name": "Chevrolet Camaro", "price": 35000, "brand": "Chevrolet", "year": 2021},
    {"name": "Honda Civic", "price": 18000, "brand": "Honda", "year": 2020},
    {"name": "Tesla Model 3", "price": 40000, "brand": "Tesla", "year": 2022},
    {"name": "BMW 3 Series", "price": 35000, "brand": "BMW", "year": 2019},
    {"name": "Audi A4", "price": 37000, "brand": "Audi", "year": 2021},
    {"name": "Mercedes-Benz C-Class", "price": 40000, "brand": "Mercedes", "year": 2022},
    {"name": "Volkswagen Golf", "price": 20000, "brand": "Volkswagen", "year": 2018},
    {"name": "Nissan Altima", "price": 17000, "brand": "Nissan", "year": 2020},
    {"name": "Subaru Impreza", "price": 22000, "brand": "Subaru", "year": 2019},
    {"name": "Hyundai Elantra", "price": 16000, "brand": "Hyundai", "year": 2020},
    {"name": "Kia Optima", "price": 19000, "brand": "Kia", "year": 2021},
    {"name": "Mazda 6", "price": 24000, "brand": "Mazda", "year": 2021},
    {"name": "Porsche 911", "price": 100000, "brand": "Porsche", "year": 2022},
    {"name": "Lexus IS", "price": 35000, "brand": "Lexus", "year": 2021},
    {"name": "Jaguar XF", "price": 45000, "brand": "Jaguar", "year": 2021},
    {"name": "Alfa Romeo Giulia", "price": 38000, "brand": "Alfa Romeo", "year": 2020},
    {"name": "Volvo S60", "price": 33000, "brand": "Volvo", "year": 2019},
    {"name": "Infiniti Q50", "price": 36000, "brand": "Infiniti", "year": 2021}
]


@lab3.route('/lab3/cars')
def index():
    return render_template('lab3/cars.html')

@lab3.route('/lab3/results')
def search():
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    filtered_cars = [
        car for car in cars
        if int(min_price) <= car['price'] <= int(max_price)
    ]

    return render_template('lab3/results.html', cars=filtered_cars)