function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(response => response.json())
    .then(films => {
        const tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        films.forEach(film => {
            const tr = document.createElement('tr');
            
            const tdTitleRus = document.createElement('td');
            const tdTitle = document.createElement('td');
            const tdYear = document.createElement('td');
            const tdActions = document.createElement('td');

            tdTitleRus.textContent = film.title_ru;
            tdTitle.innerHTML = film.title ? `<i>${film.title}</i>` : '';
            tdYear.textContent = film.year;

            const editButton = document.createElement('button');
            editButton.textContent = 'Редактировать';
            editButton.onclick = () => editFilm(film.id);

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Удалить';
            deleteButton.onclick = () => deleteFilm(film.id, film.title_ru);

            tdActions.append(editButton, deleteButton);
            tr.append(tdTitleRus, tdTitle, tdYear, tdActions);
            tbody.append(tr);
        });
    });
}

function deleteFilm(id, title) {
    if (confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList());
    }
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title_ru: document.getElementById('title-ru').value,
        title: document.getElementById('title').value,
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film)
    })
    .then(response => response.ok ? {} : response.json())
    .then(errors => {
        if (errors.title_ru) document.getElementById('title-ru-error').textContent = errors.title_ru;
        if (errors.title) document.getElementById('title-error').textContent = errors.title;
        if (errors.year) document.getElementById('year-error').textContent = errors.year;
        if (errors.description) document.getElementById('description-error').textContent = errors.description;
    })
    .finally(() => {
        fillFilmList();
        hideModal();
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(response => response.json())
    .then(film => {
        document.getElementById('id').value = id;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('title').value = film.title;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

// Копирование названия на основе поля title-ru
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('title-ru').addEventListener('blur', function () {
        const titleRu = document.getElementById('title-ru').value.trim();
        const title = document.getElementById('title');

        // Копируем русское название, если оригинальное пустое
        if (!title.value.trim()) {
            title.value = titleRu;
        }
    });
});