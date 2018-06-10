import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


BOOKS = {
    uuid.uuid4().hex: {
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Афанасьевич Булгаков',
        'read': True
    },
    uuid.uuid4().hex:
        {
            'id': uuid.uuid4().hex,
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J. K. Rowling',
            'read': False
        },
    uuid.uuid4().hex:
        {
            'id': uuid.uuid4().hex,
            'title': 'Евгений Онегин',
            'author': 'Александр Сергеевич Пушкин',
            'read': True
        }
}


def validate_book(book: dict) -> None:
    global BOOKS
    for attr in ('title', 'author'):
        if not book.get(attr):
            raise ValueError(f"{attr.title()} is required.")
    book_title: str = book['title']
    if book_title.lower() in (book['title'].lower() for book in BOOKS.values()):
        raise ValueError(f"Book '{book_title}' already exists.")


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('Pong 🏓')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    global BOOKS
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        try:
            validate_book(data)
        except ValueError as err:
            return jsonify({'status': 'error', 'message': str(err)}), 400

        BOOKS[uuid.uuid4().hex] = {
            'id': uuid.uuid4().hex,
            'title': data.get('title'),
            'author': data.get('author'),
            'read': data.get('read', False),
        }
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS

    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    global BOOKS
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        if book_id not in BOOKS:
            return jsonify({'status': 'error', 'message': 'ID not exists'}), 400

        BOOKS[book_id] = {
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        }
        response_object['message'] = 'Book updated!'
    elif request.method == 'DELETE':
        if BOOKS.pop(book_id, False):
            response_object['message'] = 'Book removed!'
        else:
            return jsonify({'status': 'error', 'message': 'ID not exists'}), 400
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
