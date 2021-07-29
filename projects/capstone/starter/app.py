from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from auth import requires_auth
from models import *
from settings import setup_db


def create_app():
    # create and configure the app
    returned_app = Flask(__name__)
    returned_app.url_map.strict_slashes = False
    setup_db(returned_app)

    # the next method will drop all the tables and recreates them and insert a single row in every table.
    # IMPORTANT: RUN ONCE OR ELSE ALL THE DATA WILL BE LOST WHEN RUNNING THE APP AGAIN
    # drop_all_create_all_add_record()

    returned_app.app_context().push()
    CORS(returned_app, resources={r"*": {"origins": '*'}})

    @returned_app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    return returned_app


app = create_app()


@app.route('/', methods=['GET', ])
def index():
    return jsonify(
        {
            "1- message": "Welcome to the library application.",
            "2- endpoints": "The endpoints of the app are:",
            "3- /authors": "to add a new author, get an author/all authors or delete an author.",
            "4- /categories": "to add a new category, get a category/all categories or delete a category.",
            "5- /book": "to add a new book, get a book/all books or delete a book.",
            "6- /borrower": "to add a new borrower, get a borrower/all borrowers or delete a borrower.",
            "7- /borrowed_books":
                "to add a new borrowed book, get a borrowed book/all borrowed books or delete a borrowed book.",
        }
    )


PER_PAGE = 10


###################################################################
# AUTHOR ENDPOINTS
###################################################################


@app.route('/authors/', methods=['GET', ])
@requires_auth('get:authors')
def authors():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', PER_PAGE, int)
    all_authors = Author.query.paginate(page=page, per_page=per_page).items
    return jsonify(
        {
            "authors": [single_author.format() for single_author in all_authors],
            "total": len(Author.query.all()),
        }
    )


@app.route('/authors/<int:author_id>/', methods=['GET', ])
@requires_auth('get:author')
def author(author_id):
    requested_author = Author.query.get_or_404(author_id)
    return jsonify(
        requested_author.format()
    )


@app.route('/authors/', methods=['POST', ])
@requires_auth('add:author')
def add_author():
    data = request.get_json()
    if 'name' not in data:
        return jsonify(
            {
                "error": "Must pass the author name in 'name'."
            }
        ), 400
    author_name = data.get('name')
    new_author = Author(name=author_name)
    try:
        new_author.insert()
        return jsonify(
            {
                "success": True,
                "message": "Author has been added successfully.",
                "total": len(Author.query.all()),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/authors/<int:author_id>/update/', methods=['PATCH', ])
@requires_auth('update:author')
def update_author(author_id):
    data = request.get_json()
    requested_author = Author.query.get_or_404(author_id)
    requested_author.name = requested_author.name if data is None else data.get(
        'name', requested_author.name)
    try:
        requested_author.update()
        return jsonify(
            {
                "success": True,
                "message": "Author has been updated successfully.",
                "author": Author.query.get_or_404(author_id).format(),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/authors/<int:author_id>/delete/', methods=['DELETE', ])
@requires_auth('delete:author')
def delete_author(author_id):
    requested_author = Author.query.get_or_404(author_id)
    try:
        requested_author.delete()
        return jsonify(
            {
                "success": True,
                "message": "Author has been deleted successfully.",
                "total": len(Author.query.all()),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


# TODO: get book of current author (DONE)
@app.route('/authors/<int:author_id>/books/', methods=['GET', ])
@requires_auth('get:author-books')
def author_books(author_id):
    Author.query.get_or_404(author_id)
    all_books = Book.query.filter(Book.author_id == author_id).all()
    try:
        return jsonify(
            {
                "success": True,
                "books": [single_book.format() for single_book in all_books],
                "total": len(all_books)
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


###################################################################
# CATEGORY ENDPOINTS
###################################################################


@app.route('/categories/', methods=['GET', ])
@requires_auth('get:categories')
def categories():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', PER_PAGE, int)
    all_categories = Category.query.paginate(page=page, per_page=per_page).items
    return jsonify(
        {
            "categories": [single_category.format() for single_category in all_categories],
            "total": len(Category.query.all())
        }
    )


@app.route('/categories/<int:category_id>/', methods=['GET', ])
@requires_auth('get:category')
def category(category_id):
    requested_category = Category.query.get_or_404(category_id)
    return jsonify(
        {
            "category": requested_category.format(),
            "success": True,
        }
    )


@app.route('/categories/', methods=['POST', ])
@requires_auth('add:category')
def add_category():
    data = request.get_json()
    if 'title' not in data:
        return jsonify(
            {
                "error": "Must pass the category title in 'title'."
            }
        ), 400
    category_title = data.get('title')
    new_category = Category(title=category_title)
    try:
        new_category.insert()
        return jsonify(
            {
                "success": True,
                "message": "Category has been added successfully.",
                "total": len(Category.query.all())
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/categories/<int:category_id>/update/', methods=['PATCH', ])
@requires_auth('update:category')
def update_category(category_id):
    data = request.get_json()
    requested_category = Category.query.get_or_404(category_id)
    requested_category.title = requested_category.title if data is None else data.get(
        'title', requested_category.title)
    try:
        requested_category.update()
        return jsonify(
            {
                "success": True,
                "message": "Category has been updated successfully.",
                "category": Category.query.get_or_404(category_id).format(),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/categories/<int:category_id>/delete/', methods=['DELETE', ])
@requires_auth('delete:category')
def delete_category(category_id):
    requested_category = Category.query.get_or_404(category_id)
    try:
        requested_category.delete()
        return jsonify(
            {
                "success": True,
                "message": "Category has been deleted successfully.",
                "total": len(Category.query.all()),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


# TODO: get books in current category (DONE)
@app.route('/categories/<int:category_id>/books/', methods=['GET', ])
@requires_auth('get:category-books')
def category_books(category_id):
    Category.query.get_or_404(category_id)
    books_of_category = Book.query.filter(Book.category_id == category_id).all()
    try:
        return jsonify(
            {
                "success": True,
                "books": [single_book.format() for single_book in books_of_category],
                "total": len(books_of_category)
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


###################################################################
# BOOKS ENDPOINTS
###################################################################


@app.route('/books/', methods=['GET', ])
@requires_auth('get:books')
def books():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', PER_PAGE, int)
    all_books = Book.query.paginate(page=page, per_page=per_page).items
    return jsonify(
        {
            "books": [single_book.format() for single_book in all_books],
            "total": len(Book.query.all())
        }
    )


@app.route('/books/<int:book_id>/', methods=['GET', ])
@requires_auth('get:book')
def book(book_id):
    requested_book = Book.query.get_or_404(book_id)
    return jsonify(
        {
            "book": requested_book.format(),
            "success": True,
        }
    )


@app.route('/books/', methods=['POST', ])
@requires_auth('add:book')
def add_book():
    data = request.get_json()
    if 'title' not in data:
        return jsonify(
            {
                "error": "Must pass the book title in 'title'."
            }
        ), 400
    book_title = data.get('title')

    if 'pages' not in data:
        return jsonify(
            {
                "error": "Must pass the book pages in 'pages'."
            }
        ), 400
    book_pages = data.get('pages')

    if 'about' not in data:
        return jsonify(
            {
                "error": "Must pass the book about in 'about'."
            }
        ), 400
    book_about = data.get('about')

    if 'author_id' not in data:
        return jsonify(
            {
                "error": "Must pass the book author_id in 'author_id'."
            }
        ), 400
    book_author = int(data.get('author_id'))

    author_ids = [
        single_author.id for single_author in Author.query.distinct(Author.id).all()]
    if book_author not in author_ids:
        return jsonify(
            {
                "error": True,
                "author_ids": author_ids,
                "message": "author id must be in author ids.",
            }
        ), 400

    if 'category_id' not in data:
        return jsonify(
            {
                "error": "Must pass the book category_id in 'category_id'."
            }
        ), 400
    book_category = int(data.get('category_id'))

    category_ids = [
        single_category.id for single_category in Category.query.distinct(Category.id).all()]
    if book_category not in category_ids:
        return jsonify(
            {
                "error": True,
                "category_ids": category_ids,
                "message": "category id must be in category ids.",
            }
        ), 400

    new_book = Book(
        title=book_title,
        pages=book_pages,
        about=book_about,
        category=Category.query.get_or_404(book_category),
        author=Author.query.get_or_404(book_author)
    )
    try:
        new_book.insert()
        return jsonify(
            {
                "success": True,
                "message": "Book has been added successfully.",
                "total": len(Book.query.all())
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/books/<int:book_id>/update/', methods=['PATCH', ])
@requires_auth('update:book')
def update_book(book_id):
    data = request.get_json()
    requested_book = Book.query.get_or_404(book_id)

    try:
        requested_book.title = requested_book.title if data is None else data.get(
            'title', requested_book.title)
        requested_book.pages = requested_book.pages if data is None else data.get(
            'pages', requested_book.pages)
        requested_book.about = requested_book.about if data is None else data.get(
            'about', requested_book.about)

        author_ids = [
            single_author.id for single_author in Author.query.distinct(Author.id).all()]
        book_author = requested_book.author_id if data is None else data.get(
            'author_id', requested_book.author_id)
        if book_author not in author_ids:
            return jsonify(
                {
                    "error": True,
                    "author_ids": author_ids,
                    "message": "author id must be in author ids.",
                }
            ), 400

        book_category = requested_book.category_id if data is None else data.get(
            'category_id', requested_book.category_id)
        category_ids = [
            single_category.id for single_category in Category.query.distinct(Category.id).all()]
        if book_category not in category_ids:
            return jsonify(
                {
                    "error": True,
                    "category_ids": category_ids,
                    "message": "category id must be in category ids.",
                }
            ), 400

        requested_book.author = Author.query.get_or_404(book_author)
        requested_book.category = Category.query.get_or_404(book_category)
        requested_book.update()
        return jsonify(
            {
                "success": True,
                "message": "Book has been updated successfully.",
                "book": Book.query.get_or_404(book_id).format()
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/books/<int:book_id>/delete/', methods=['DELETE', ])
@requires_auth('delete:book')
def delete_book(book_id):
    requested_book = Book.query.get_or_404(book_id)
    try:
        requested_book.delete()
        return jsonify(
            {
                "success": True,
                "message": "Book has been deleted successfully.",
                "total": len(Book.query.all()),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


# TODO: get borrowers of current book (DONE)
@app.route('/books/<int:book_id>/borrowers/', methods=['GET', ])
@requires_auth('get:book-borrowers')
def book_borrowers(book_id):
    borrowers_of_book = Borrower.query.join(BorrowedBooks).filter(
        BorrowedBooks.book_id == book_id).all()
    try:
        return jsonify(
            {
                "total_borrowers": len(borrowers_of_book),
                "borrowers": [single_borrower.format() for single_borrower in borrowers_of_book],
                "success": True,
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


###################################################################
# BORROWERS ENDPOINTS
###################################################################


@app.route('/borrowers/', methods=['GET', ])
@requires_auth('get:borrowers')
def borrowers():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', PER_PAGE, int)
    all_borrowers = Borrower.query.paginate(page=page, per_page=per_page).items
    return jsonify(
        {
            "borrowers": [single_borrower.format() for single_borrower in all_borrowers],
            "total": len(Borrower.query.all())
        }
    )


@app.route('/borrowers/<int:borrower_id>/', methods=['GET', ])
@requires_auth('get:borrower')
def borrower(borrower_id):
    requested_borrower = Borrower.query.get_or_404(borrower_id)
    return jsonify(
        {
            "success": True,
            "borrower": requested_borrower.format(),
        }
    )


@app.route('/borrowers/', methods=['POST', ])
@requires_auth('add:borrower')
def add_borrower():
    data = request.get_json()

    if 'name' not in data:
        return jsonify(
            {
                "error": "Must pass the borrower name in 'name'."
            }
        ), 400
    borrower_name = request.get_json().get('name')

    new_borrower = Borrower(
        name=borrower_name
    )
    try:
        new_borrower.insert()
        return jsonify(
            {
                "success": True,
                "message": "Borrower has been added successfully.",
                "total": len(Borrower.query.all())
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/borrowers/<int:borrower_id>/update/', methods=['PATCH', ])
@requires_auth('update:borrower')
def update_borrower(borrower_id):
    requested_borrower = Borrower.query.get_or_404(borrower_id)
    data = request.get_json()
    requested_borrower.name = requested_borrower.name if data is None else data.get(
        'name', requested_borrower.name)
    try:
        requested_borrower.update()
        return jsonify(
            {
                "success": True,
                "message": "Borrower has been Updated successfully.",
                "borrower": Borrower.query.get_or_404(borrower_id).format()
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/borrowers/<int:borrower_id>/delete/', methods=['DELETE', ])
@requires_auth('delete:borrower')
def delete_borrower(borrower_id):
    requested_borrower = Borrower.query.get_or_404(borrower_id)
    try:
        requested_borrower.delete()
        return jsonify(
            {
                "success": True,
                "message": "Borrower has been deleted successfully.",
                "total": len(Borrower.query.all()),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


# TODO: get books of current borrower (Done)
@app.route('/borrowers/<int:borrower_id>/books/', methods=['GET', ])
@requires_auth('get:borrower-books')
def borrower_books(borrower_id):
    books_of_borrower = Book.query.join(BorrowedBooks).filter(
        BorrowedBooks.borrower_id == borrower_id).all()
    return jsonify(
        {
            "success": True,
            "books": [single_book.format() for single_book in books_of_borrower],
            "total": len(books_of_borrower),
        }
    )


###################################################################
# BORROWED BOOKS ENDPOINTS
###################################################################


@app.route('/borrowed_books/', methods=['GET', ])
@requires_auth('get:borrowed_books')
def borrowed_books():
    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', PER_PAGE, int)
    all_borrowed_books = BorrowedBooks.query.paginate(
        page=page, per_page=per_page).items
    return jsonify(
        {
            "borrowed_books": [single_borrowed_book.format() for single_borrowed_book in all_borrowed_books],
            "total": len(BorrowedBooks.query.all())
        }
    )


@app.route('/borrowed_books/<int:borrowed_book_id>/', methods=['GET', ])
@requires_auth('get:borrowed_book')
def borrowed_book(borrowed_book_id):
    requested_borrowed_book = BorrowedBooks.query.get_or_404(borrowed_book_id)
    return jsonify(
        {
            "success": True,
            "borrowed_book": requested_borrowed_book.format(),
        }
    )


@app.route('/borrowed_books/', methods=['POST', ])
@requires_auth('add:borrowed_book')
def add_borrowed_book():
    data = request.get_json()
    if 'book_id' not in data:
        return jsonify(
            {
                "error": True,
                "message": "Must pass book id in 'book_id'.",
            }
        ), 400

    if 'borrower_id' not in data:
        return jsonify(
            {
                "error": True,
                "message": "Must pass borrower id in 'borrower_id'.",
            }
        ), 400

    book_id = int(data.get('book_id'))
    book_ids = [single_book.id for single_book in Book.query.distinct(Book.id).all()]
    if book_id not in book_ids:
        return jsonify(
            {
                "error": True,
                "books_ids": book_ids,
                "message": "book id must be in books ids.",
            }
        ), 400

    borrower_id = int(data.get('borrower_id'))
    borrowers_ids = [
        single_borrower.id for single_borrower in Borrower.query.distinct(Borrower.id).all()]
    if borrower_id not in borrowers_ids:
        return jsonify(
            {
                "error": True,
                "borrowers_ids": borrowers_ids,
                "message": "borrower id must be in borrowers ids.",
            }
        ), 400

    new_borrowed_book = BorrowedBooks(
        book_id=book_id,
        borrower_id=borrower_id
    )
    try:
        new_borrowed_book.insert()
        return jsonify(
            {
                "success": True,
                "message": "Borrowed Book has been added successfully.",
                "total": len(BorrowedBooks.query.all())
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/borrowed_books/<int:borrowed_book_id>/update/', methods=['PATCH', ])
@requires_auth('update:borrowed_book')
def update_borrowed_book(borrowed_book_id):
    data = request.get_json()

    requested_borrowed_book = BorrowedBooks.query.get_or_404(borrowed_book_id)
    book_id = requested_borrowed_book.book_id if data is None else int(
        data.get('book_id'))

    book_ids = [single_book.id for single_book in Book.query.distinct(Book.id).all()]
    if book_id not in book_ids:
        return jsonify(
            {
                "error": True,
                "books_ids": book_ids,
                "message": "book id must be in books ids.",
            }
        ), 400

    borrower_id = requested_borrowed_book.borrower_id if data is None else int(
        data.get('borrower_id'))
    borrowers_ids = [
        single_borrower.id for single_borrower in Borrower.query.distinct(Borrower.id).all()]
    if borrower_id not in borrowers_ids:
        return jsonify(
            {
                "error": True,
                "borrowers_ids": borrowers_ids,
                "message": "borrower id must be in borrowers ids.",
            }
        ), 400
    requested_borrowed_book.book_id = book_id
    requested_borrowed_book.borrower_id = borrower_id
    try:
        requested_borrowed_book.update()
        return jsonify(
            {
                "success": True,
                "message": "Borrowed Book has been updated successfully.",
                "total": len(BorrowedBooks.query.all()),
                "borrowed_book": BorrowedBooks.query.get_or_404(borrowed_book_id).format(),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


@app.route('/borrowed_books/<int:borrowed_book_id>/delete/', methods=['DELETE', ])
@requires_auth('delete:borrowed_book')
def delete_borrowed_book(borrowed_book_id):
    requested_borrowed_book = BorrowedBooks.query.get_or_404(borrowed_book_id)
    try:
        requested_borrowed_book.delete()
        return jsonify(
            {
                "success": True,
                "message": "Borrowed Book has been deleted successfully.",
                "total": len(BorrowedBooks.query.all()),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


# TODO: update the rating of the book and the return time (Done)
@app.route('/borrowed_books/<int:borrowed_book_id>/return/', methods=['PATCH', ])
@requires_auth('update:borrowed_book')
def return_borrowed_book(borrowed_book_id):
    data = request.get_json()

    requested_borrowed_book = BorrowedBooks.query.get_or_404(borrowed_book_id)
    if 'rating' not in data:
        return jsonify(
            {
                "error": "Must pass the rating in 'rating'."
            }
        ), 400
    if not (0 <= float(data.get('rating')) <= 10):
        return jsonify(
            {
                "error": "Rating must be between 0 and 10"
            }
        ), 400

    requested_borrowed_book.returned_at = datetime.datetime.now()
    requested_borrowed_book.rating = data.get('rating')
    try:
        requested_borrowed_book.update()
        return jsonify(
            {
                "success": True,
                "message": "Borrowed Book has been updated successfully.",
                "total": len(BorrowedBooks.query.all()),
                "borrowed_book": BorrowedBooks.query.get_or_404(borrowed_book_id).format(),
            }
        )
    except:
        abort(422)
    finally:
        db.session.close()


###################################################################
# EXCEPTIONS
###################################################################


@app.errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            "message": "bad request",
            "error": 400,
        }
    ), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify(
        {
            "message": "unauthorized",
            "error": 401,
        }
    ), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify(
        {
            "message": "forbidden",
            "error": 403,
        }
    ), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "message": "not found",
            "error": 404,
        }
    ), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "message": "method not allowed",
            "error": 405,
        }
    ), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify(
        {
            "message": "unprocessable",
            "error": 422,
        }
    ), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify(
        {
            "message": "server error",
            "error": 500,
        }
    ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
