from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.step2', name=name))
    return render_template('lab9/index.html')

@lab9.route('/lab9/step2', methods=['GET', 'POST'])
def step2():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.step3', name=name, age=age))
    return render_template('lab9/step2.html', name=name)

@lab9.route('/lab9/step3', methods=['GET', 'POST'])
def step3():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.step4', name=name, age=age, gender=gender))
    return render_template('lab9/step3.html', name=name, age=age)

@lab9.route('/lab9/step4', methods=['GET', 'POST'])
def step4():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        choice1 = request.form.get('choice1')
        return redirect(url_for('lab9.step5', name=name, age=age, gender=gender, choice1=choice1))
    return render_template('lab9/step4.html', name=name, age=age, gender=gender)

@lab9.route('/lab9/step5', methods=['GET', 'POST'])
def step5():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    choice1 = request.args.get('choice1')
    if request.method == 'POST':
        choice2 = request.form.get('choice2')
        return redirect(url_for('lab9.result', name=name, age=age, gender=gender, choice1=choice1, choice2=choice2))
    return render_template('lab9/step5.html', name=name, age=age, gender=gender, choice1=choice1)

@lab9.route('/lab9/result')
def result():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    choice1 = request.args.get('choice1')  # что-то вкусное или красивое
    choice2 = request.args.get('choice2')  # сладкое/сытное или цветы/украшения

    if choice1 == 'tasty':
        if choice2 == 'sweet':
            gift = 'мешочек конфет'
            image = 'konfeti2.jpg'
        else: 
            gift = 'сытное блюдо'
            image = 'sytnoy.jpeg'
    else: 
        if choice2 == 'flowers':
            gift = 'букет цветов'
            image = 'flower.jpg'
        else: 
            gift = 'украшение'
            image = 'decor.jpg'

    if gender == 'male':
        pronoun = 'ты'
        grew = 'вырос'
        smart = 'умным'
        was = 'был'
    else:
        pronoun = 'ты'
        grew = 'выросла'
        smart = 'умной'
        was = 'была'

    message = f"Поздравляю тебя, {name}, желаю, чтобы {pronoun} быстро {grew}, {was} {smart}. Вот тебе подарок — {gift}."

    return render_template('lab9/result.html', message=message, image=image)