from flask import Blueprint, render_template, request, jsonify, abort
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "The Substance",
        "title_ru":"СУБСТАНЦИЯ",
        "year": 2024,
        "description": "Слава голливудской звезды Элизабет Спаркл осталась в \
            прошлом, хоть она всё ещё ведёт популярное фитнес-шоу на телевидении. \
            Когда её передачу собираются перезапустить с новой звездой, Элизабет \
            решает принять уникальный препарат «Субстанция». Так на свет появляется\
            молодая и сексуальная Сью. Однако у совершенства есть своя цена, и расплата\
            не заставит себя долго ждать."
    },
    {
        "title": "Divergent",
        "title_ru":"ДИВЕРГЕНТ",
        "year": 2014,
        "description": "В антиутопическом Чикаго будущего общество разделено на пять \
            фракций: «Эрудиция», «Дружелюбие», «Искренность», «Отречение» и «Бесстрашие». \
            Каждый житель, достигший 16 лет, должен пройти тест, чтобы определить, к какой \
            фракции он принадлежит."
    },
    {
        "title": "Euphoria",
        "title_ru":"Эйфория",
        "year": 2019,
        "description": "17-летняя Ру Беннетт возвращается домой после лечения в \
        реабилитационной клинике. Не теряя времени, она опять берется за старые \
        привычки — наркотики и тусовки. Однако появление в городе девушки Джулс \
        становится для Ру знаком надежды."
    },
    {
        "title": "Dorian Gray",
        "title_ru":"Дориан Грей",
        "year": 2009,
        "description": "Оливер Паркер в третий раз переносит тексты Уайльда на экран \
        (до этого были пьесы «Идеальный муж» и «Как важно быть серьезным») и каждый раз \
        привлекает Колина Ферта. В этот раз актер Ферт играет лорда Генри Уоттона, а \
        заглавного героя — Бен Барнс, знакомый ролью принца Каспиана. Паркер верен \
        роману, но в нюансах отходит от него: добавляет хоррора и эротики, придавая \
        сюжету остроты и динамики"
    },
    {
        "title": "Paddington",
        "title_ru":"Приключения Паддингтона",
        "year": 2014,
        "description": "Первая экранизация популярной в Англии книг Майкла Бонда \
            про мишку-путешественника умилила дочку писателя — та на премьере не \
            сдержала слез. Трогательная забавная история получилась в эстетике Уэса \
            Андерсона и показала, каким разным может быть Лондон: то нелепым и блеклым, \
            то волшебным и ярким. В роли злодейки-таксидермистки — Николь Кидман, \
            которая сама с детства любила Паддингтона."
    }
]


def is_valid_year(year):
    year = int(year)  # Преобразование в целое число
    current_year = datetime.now().year
    return 1895 <= year <= current_year


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def git_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film_by_id(id):
    if 0 <= id < len(films):
        return jsonify(films[id])
    else:
        abort(404)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        abort(404)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()

        # Проверка полей
        if not film.get('title_ru') or not film['title_ru'].strip():
            return {'title_ru': 'Русское название обязательно'}, 400

        # Если русское название пустое, то проверяем оригинальное
        if not film.get('title') and not film.get('title_ru'):
            return {'title': 'Оригинальное название обязательно, если русское пустое'}, 400

        if not film.get('year') or not is_valid_year(film['year']):
            return {'year': 'Год должен быть в пределах от 1895 до текущего года'}, 400

        if not film.get('description') or not film['description'].strip():
            return {'description': 'Описание обязательно'}, 400

        if len(film['description']) > 2000:
            return {'description': 'Описание не должно превышать 2000 символов'}, 400

        films[id] = film
        return jsonify(films[id])
    else:
        abort(404)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()  # Получение данных из тела запроса

    # Проверка полей
    if not film.get('title_ru') or not film['title_ru'].strip():
        return {'title_ru': 'Русское название обязательно'}, 400

    # Если русское название пустое, то проверяем оригинальное
    if not film.get('title') and not film.get('title_ru'):
        return {'title': 'Оригинальное название обязательно, если русское пустое'}, 400

    if not film.get('year') or not is_valid_year(film['year']):
        return {'year': 'Год должен быть в пределах от 1895 до текущего года'}, 400

    if not film.get('description') or not film['description'].strip():
        return {'description': 'Описание обязательно'}, 400

    if len(film['description']) > 2000:
        return {'description': 'Описание не должно превышать 2000 символов'}, 400

    films.append(film)  # Добавляем фильм в конец списка
    new_index = len(films) - 1  # Возвращаем индекс нового фильма
    return jsonify({"id": new_index}), 201


