The capstone project is a system for a library

Motivation:
I was imagining making an application for a library that serves many users, that's why I implemented it.


Ahe app is hosted on heruko `https://fsnd-library-api.herokuapp.com/`


The library has the following:


1. manager: who has all the privileges on the system <br>
can add authors, books, categories, borrowers (users who borrow books) and record (add) borrowing operations <br>
can update authors, books, categories, borrowers (users who borrow books) and record (add) borrowing operations <br>
can delete authors, books, categories, borrowers (users who borrow books) and record (add) borrowing operations <br>
can see all authors, books, categories, borrowers (users who borrow books) and record (add) borrowing operations <br>


2. author: who has some privileges on the system <br>
can add books he wrote and borrow a book from the library <br>
can update books he wrote and return a book he borrowed back to the library <br>
can delete books he wrote <br>
can see his data, and the books he wrote <br>
can see all authors names, books, and categories <br>


3. borrower: he is the person who borrow books from the library, he has some privileges on the system <br>
can see all authors names, books, and categories <br>
can borrow a book <br>
can update his data <br>
can return books he borrowed and rate them <br>

### Installing Dependencies for the Backend

1. **Python 3** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```

4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the library.psql file provided, run in terminal:
```bash
createdb library
psql library < library.psql
```

### Running the server

From within the `./starter` directory, first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Endpoints docs

### the root endpoint /
```
GET /
- The welcome message
- Request Arguments: None
- Returns: an object welcoming the user with the endpoints of the application.

{
  "1- message": "Welcome to the library application.",
  "2- endpoints": "The endpoints of the app are:",
  "3- /authors": "to add a new author, get an author/all authors or delete an author.",
  "4- /categories": "to add a new category, get a category/all categories or delete a category.",
  "5- /book": "to add a new book, get a book/all books or delete a book.",
  "6- /borrower": "to add a new borrower, get a borrower/all borrowers or delete a borrower.",
  "7- /borrowed_books": "to add a new borrowed book, get a borrowed book/all borrowed books or delete a borrowed book."
}
```

### the authors' endpoint /authors
```
GET /authors/
- Fetches a dictionary of all the authors name and the number of books an author wrote, paginated 10 authors per page
- Request Arguments: 
    page, which indicate the number of the current page (OPTIONAL)
    per_page, which indicate the number of result per page (OPTIONAL)
- Returns: 
    1- an object authors, contains all the authors' names and number of book written, per current page.
    2- an object total, which indicates the total authors in the table.
{
    "authors": [
        {
            "id": 1,
            "name": "Abdullah",
            "number_of_written_books": 1
        }
    ],
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:authors' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


GET /authors/<int:author_id>/
- Fetches the requested author
- Requested Arguments: the author_id number
- Returns:
    1- an object author, which contains the id, name and the number of written book ok the author
{
    "id": 1,
    "name": "Abdullah",
    "number_of_written_books": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:authors' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested author doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


POST /authors/
- Add a new author to the database.
- Requested Arguments: name of the author
- Return: an object which is a success state, message and the total authors in the database
{
    "message": "Author has been added successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have the 'name', the endpoint will throw 400
{
    "error": "Must pass the author name in 'name'."
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'add:author' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a POST method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while adding the author, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}


PATCH /authors/<int:author_id>/update/
- Update an author in the database.
- Requested Arguments: name of the author
- Return: an object which is a success state, message and the total authors in the database
{
    "message": "Author has been updated successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'update:author' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested author doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a PATCH method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while updating the author, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}


DELETE /authors/<int:author_id>/delete/
- Delete an author from the database.
- Requested Arguments: id of the author
- Return: an object which is a success state, message and the total authors in the database
{
    "message": "Author has been deleted successfully.",
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'delete:author' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested author doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a DELETE method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while deleting the author, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}


GET /authors/<int:author_id>/books/
- Fetch the books of the requested author from the database.
- Requested Arguments: id of the author
- Return: an object which has the books of the author, a success state, and the total of books of the requested author
{
    "books": [
        {
            "about": "How to program in Java",
            "author": "Abdullah",
            "category": "Programming",
            "id": 1,
            "number_of_borrowed_times": 1,
            "pages": 60,
            "rating": "0.0 of 10",
            "title": "Java"
        }
    ],
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:author-books' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested author doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}
```

### the categories' endpoint /categories
```
GET /categories/
- Fetches a dictionary of all the categories names and the number of books in every category, paginated 10 categories per page
- Request Arguments: 
    page, which indicate the number of the current page (OPTIONAL)
    per_page, which indicate the number of result per page (OPTIONAL)
- Returns: 
    1- an object categories, contains all the categories' names and number of books, per current page.
    2- an object total, which indicates the total categories in the table.
{
    "categories": [
        {
            "id": 1,
            "number_of_books": 1,
            "title": "Programming"
        }
    ],
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:categories' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

GET /categories/<int:category_id>/
- Fetches the requested category
- Requested Arguments: the category_id number
- Returns:
    1- an object category, which contains the id, title and the number of books in the category
{
    "category": {
        "id": 1,
        "number_of_books": 1,
        "title": "Programming"
    },
    "success": true
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:category' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested category doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


POST /categories/
- Add a new category to the database.
- Requested Arguments: title of the category
- Return: an object which is a success state, message and the total categories in the database
{
    "message": "Category has been added successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have the 'title', the endpoint will throw 400
{
    "error": "Must pass the category title in 'title'."
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'add:category' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a POST method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while adding the category, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

PATCH /categories/<int:category_id>/update/
- Update a category in the database.
- Requested Arguments: title of the category
- Return: an object which is a success state, message and the total categories in the database
{
    "message": "Category has been updated successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'update:category' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested category doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a PATCH method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while updating the category, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

DELETE /categories/<int:category_id>/delete/
- Delete a category from the database.
- Requested Arguments: id of the category
- Return: an object which is a success state, message and the total categories in the database
{
    "message": "Category has been deleted successfully.",
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'delete:category' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested category doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a DELETE method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while deleting the category, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

GET /categories/<int:category_id>/books/
- Fetch the books of the requested category from the database.
- Requested Arguments: id of the category
- Return: an object which has the books of the category, a success state, and the total of books of the requested category
{
    "books": [
        {
            "about": "How to program in Java",
            "author": "Abdullah",
            "category": "Programming",
            "id": 1,
            "number_of_borrowed_times": 1,
            "pages": 60,
            "rating": "0.0 of 10",
            "title": "Java"
        }
    ],
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:category-books' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested category doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


```

### the books' endpoint /books
```
GET /books/
- Fetches a dictionary of all the books and the number of books in the database, paginated 10 books per page
- Request Arguments: 
    page, which indicate the number of the current page (OPTIONAL)
    per_page, which indicate the number of result per page (OPTIONAL)
- Returns: 
    1- an object books, contains all the books' info, per current page.
    2- an object total, which indicates the total books in the table.
{
    "books": [
        {
            "about": "How to program in Java",
            "author": "Abdullah",
            "category": "Programming",
            "id": 1,
            "number_of_borrowed_times": 1,
            "pages": 60,
            "rating": "0.0 of 10",
            "title": "Java"
        }
    ],
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:books' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

GET /books/<int:book_id>/
- Fetches the requested book
- Requested Arguments: the book_id number
- Returns:
    1- an object book, which contains the book info
{
    "book": {
        "about": "How to program in Java",
        "author": "Abdullah",
        "category": "Programming",
        "id": 1,
        "number_of_borrowed_times": 1,
        "pages": 60,
        "rating": "0.0 of 10",
        "title": "Java"
    },
    "success": true
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested book doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


POST /books/
- Add a new book to the database.
- Requested Arguments:
    title of the book
    pages (i.e number of pages) of the book
    about (i.e summary) of the book
    author_id
    category_id
- Return: an object which is a success state, message and the total books in the database
{
    "message": "Book has been added successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have the 'title', the endpoint will throw 400
{
    "error": "Must pass the book title in 'title'."
}

if the request doesn't have the 'pages', the endpoint will throw 400
{
    "error": "Must pass the book pages in 'pages'."
}

if the request doesn't have the 'about', the endpoint will throw 400
{
    "error": "Must pass the book about in 'about'."
}

if the request doesn't have the 'author_id', the endpoint will throw 400
{
    "error": "Must pass the book author_id in 'author_id'."
}

if the given author_id doesn't belong to any author, the endpoint will throw 400
and view the registered author_id
{
    "error": True,
    "author_ids": [1, 2, 3, 4], (e.g if we have 4 authors registered)
    "message": "author id must be in author ids.",
}

if the request doesn't have the 'category_id', the endpoint will throw 400
{
    "error": "Must pass the book category_id in 'category_id'."
}

if the given category_id doesn't belong to any category, the endpoint will throw 400
and view the registered category_id
{
    "error": True,
    "category_ids": [1, 2], (e.g if we have 2 categories registered)
    "message": "category id must be in category ids.",
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'add:book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a POST method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while adding the book, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

PATCH /books/<int:book_id>/update/
- Update a book in the database.
- Requested Arguments: 
    title of the book (OPTIONAL)
    pages (i.e number of pages) of the book (OPTIONAL)
    about (i.e summary) of the book (OPTIONAL)
    author_id (OPTIONAL)
    category_id (OPTIONAL)
- Return: an object which is a success state, message and the total books in the database
{
    "message": "Book has been updated successfully.",
    "success": true,
    "total": 2
}

if the given author_id doesn't belong to any author, the endpoint will throw 400
and view the registered author_id
{
    "error": True,
    "author_ids": [1, 2, 3, 4], (e.g if we have 4 authors registered)
    "message": "author id must be in author ids.",
}

if the given category_id doesn't belong to any category, the endpoint will throw 400
and view the registered category_id
{
    "error": True,
    "category_ids": [1, 2], (e.g if we have 2 categories registered)
    "message": "category id must be in category ids.",
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'update:book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested book doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a PATCH method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while updating the book, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

DELETE /books/<int:book_id>/delete/
- Delete a book from the database.
- Requested Arguments: id of the book
- Return: an object which is a success state, message and the total books in the database
{
    "message": "Book has been deleted successfully.",
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'delete:book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested book doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a DELETE method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while deleting the book, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

GET /books/<int:book_id>/borrowers/
- Fetch the borrowers of the requested book from the database.
- Requested Arguments: id of the book
- Return: an object which has the borrowers of the book, a success state, and the total of borrowers of the requested book
{
    "borrowers": [
        {
            "id": 1,
            "name": "Nasser",
            "number_of_borrowed_books": 1
        }
    ],
    "success": true,
    "total_borrowers": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:book-borrowers' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested book doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

```

### the borrowers' endpoint /borrowers
```
GET /borrowers/
- Fetches a dictionary of all the borrowers and the number of borrowers in the database, paginated 10 books per page
- Request Arguments: 
    page, which indicate the number of the current page (OPTIONAL)
    per_page, which indicate the number of result per page (OPTIONAL)
- Returns: 
    1- an object borrowers, contains all the borrowers' info, per current page.
    2- an object total, which indicates the total borrowers in the table.
{
    "borrowers": [
        {
            "id": 1,
            "name": "Nasser",
            "number_of_borrowed_books": 1
        }
    ],
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:borrowers' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

GET /borrowers/<int:borrower_id>/
- Fetches the requested borrower
- Requested Arguments: the borrower_id number
- Returns:
    1- an object borrower, which contains the borrower info
{
    "borrower": {
        "id": 1,
        "name": "Nasser",
        "number_of_borrowed_books": 1
    },
    "success": true
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:borrower' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrower doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


POST /borrowers/
- Add a new borrower to the database.
- Requested Arguments: name of the borrower
- Return: an object which is a success state, message and the total borrowers in the database
{
    "message": "Book has been added successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have the 'title', the endpoint will throw 400
{
    "error": "Must pass the borrower name in 'name'."
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'add:borrower' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a POST method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while adding the borrower, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

PATCH /borrowers/<int:borrower_id>/update/
- Update a borrower in the database.
- Requested Arguments: 
    borrower_id
    name (OPTIONAL)
- Return: an object which is a success state, message and the total borrowers in the database
{
    "message": "Borrower has been Updated successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'update:borrower' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrower doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a PATCH method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while updating the borrower, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

DELETE /borrowers/<int:borrower_id>/delete/
- Delete a borrower from the database.
- Requested Arguments: id of the borrower
- Return: an object which is a success state, message and the total borrowers in the database
{
    "message": "Borrower has been deleted successfully.",
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'delete:borrower' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrower doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a DELETE method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while deleting the borrower, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

GET /borrowers/<int:borrower_id>/books/
- Fetch the books that has been borrowed by the requested borrower from the database.
- Requested Arguments: id of the borrower
- Return: an object which has the books of the request borrower, a success state, and the total books the borrower has borrowed
{
    "books": [
        {
            "about": "How to program in Java",
            "author": "Abdullah",
            "category": "Programming",
            "id": 1,
            "number_of_borrowed_times": 1,
            "pages": 60,
            "rating": "0.0 of 10",
            "title": "Java"
        }
    ],
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:borrower-books' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrower doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

```

### the borrowed_books' endpoint /borrowed_books
```
GET /borrowed_books/
- Fetches a dictionary of all the borrowing operation the happend in the library with total number, paginated 10 books per page
- Request Arguments: 
    page, which indicate the number of the current page (OPTIONAL)
    per_page, which indicate the number of result per page (OPTIONAL)
- Returns: 
    1- an object borrowed_books contains per current page:
        the book name
        the borrower name
        the date the book has been borrowed at
        the date the book has been returned at
        the rating after returning the book
    2- an object total, which indicates the total borrowers in the table.
{
    "borrowed_books": [
        {
            "book": {
                "id": 1,
                "title": "Java"
            },
            "borrowed_at": "Thu, 29 Jul 2021 11:19:00 GMT",
            "borrowed_by": {
                "id": 1,
                "name": "Nasser"
            },
            "id": 1,
            "rated": 0.0,
            "returned at": "not returned yet"
        }
    ],
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:borrowed_books' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

GET /borrowed_books/<int:borrowed_book_id>/
- Fetches the requested a specific borrowing operation
- Requested Arguments: the borrowed_book_id number
- Returns:
    1- an object borrowed book, which contains the operation info info
{
    "borrowed_book": {
        "book": {
            "id": 1,
            "title": "Java"
        },
        "borrowed_at": "Thu, 29 Jul 2021 11:19:00 GMT",
        "borrowed_by": {
            "id": 1,
            "name": "Nasser"
        },
        "id": 1,
        "rated": 0.0,
        "returned at": "not returned yet"
    },
    "success": true
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:borrowed_book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrowing operation <id> doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a GET method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}


POST /borrowed_books/
- Add a new borrowing operation to the database.
- Requested Arguments:
    book_id
    borrower_id
- Return: an object which is a success state, message and the total borrowers in the database
{
    "message": "Borrowed Book has been added successfully.",
    "success": true,
    "total": 2
}

if the request doesn't have the 'book_id', the endpoint will throw 400
{
    "error": "Must pass book id in 'book_id'.",
}

if the given book_id doesn't belong to any book, the endpoint will throw 400
and view the registered book_id
{
    "error": True,
    "book_ids": [1, 2, 3], (e.g if we have 3 books registered)
    "message": "book id must be in book ids.",
}

if the request doesn't have the 'book_id', the endpoint will throw 400
{
    "error": "Must pass book id in 'book_id'.",
}

if the given borrower_id doesn't belong to any borrower, the endpoint will throw 400
and view the registered borrower_id
{
    "error": True,
    "borrower_ids": [1, 2, 3], (e.g if we have 3 borrowers registered)
    "message": "borrower id must be in borrowers ids.",
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'add:borrowed_book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the request is not a POST method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while adding the borrower, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

PATCH /borrowed_books/<int:borrowed_book_id>/update/
- Update a borrowing operation in the database. (e.g changing the borrower or the book)
- Requested Arguments: 
    borrowed_book_id
    book_id (OPTIONAL)
    borrower_id (OPTIONAL)
- Return: an object which is a success state, message and the total borrowers in the database
{
    "message": "Borrowed Book has been updated successfully.",
    "success": true,
    "total": 2
}

if the given book_id doesn't belong to any book, the endpoint will throw 400
and view the registered book_id
{
    "error": True,
    "book_ids": [1, 2, 3], (e.g if we have 3 books registered)
    "message": "book id must be in book ids.",
}

if the given borrower_id doesn't belong to any borrower, the endpoint will throw 400
and view the registered borrower_id
{
    "error": True,
    "borrower_ids": [1, 2, 3], (e.g if we have 3 borrowers registered)
    "message": "borrower id must be in borrowers ids.",
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'update:borrowed_book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrowing operation <id> doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a PATCH method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while updating the borrower, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

DELETE /borrowed_books/<int:borrowed_book_id>/delete/
- Delete a borrowing operation from the database.
- Requested Arguments: borrowed_book_id of the borrowing operation
- Return: an object which is a success state, message and the total of borrowing operation in the database
{
    "message": "Borrowed Book has been deleted successfully.",
    "success": true,
    "total": 1
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'delete:borrowed_book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrowing operation <id> doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a DELETE method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

if any error happend while deleting the borrowing record, the endpoint will throw 422
{
    "error": 422
    "message": "unprocessable",
}

PATCH /borrowed_books/<int:borrowed_book_id>/return/
- Update (Return) a books that has been borrowed in the database.
- Requested Arguments: 
    borrowed_book_id <id> of the of the borrowing operation
    rating, to rate the book after returning it, and must be between 0 and 10
- Return: an object which has the borrowing operation contains:
    the book which has been borrowed
    the borrowing datetime
    the borrower info
    the rating of the book
    the returning datetime
    a success state, and the total number of borrowing operation.
{
    "borrowed_book": {
        "book": {
            "id": 1,
            "title": "Java"
        },
        "borrowed_at": "Thu, 29 Jul 2021 11:19:00 GMT",
        "borrowed_by": {
            "id": 1,
            "name": "Nasser"
        },
        "id": 1,
        "rated": 6.2,
        "returned at": "Thu, 29 Jul 2021 20:31:46 GMT"
    },
    "message": "Borrowed Book has been updated successfully.",
    "success": true,
    "total": 1
}

if the request doesn't have the 'rating', the endpoint will throw 400
{
    "error": "Must pass the rating in 'rating'."
}

if the request has rating, but the rating less than 0 or greater than 10, the endpoint will throw 400
{
    "error": "Rating must be between 0 and 10"
}

if the request doesn't have a token, the endpoint will throw 401
{
    "error": 401,
    "message": "unauthorized"
}

if the request doesn't have 'get:borrowed_book' permission, the endpoint will throw 403
{
    "error": 403,
    "message": "forbidden"
}

if the requested borrowing operation <id> doesn't exist, the endpoint will throw 404
{
    "error": 404,
    "message": "not found"
}

if the request is not a PATCH method, the endpoint will throw 405
{
    "error": 405,
    "message": "method not allowed"
}

```
