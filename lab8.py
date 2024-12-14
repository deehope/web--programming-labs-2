from flask import Blueprint, session, render_template

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', login = session.get('login'))

# @lab8.route('/lab8/register')


# @lab8.route('/lab8/login')


# @lab8.route('/lab8/articles')


# @lab8.route('/lab8/create')
