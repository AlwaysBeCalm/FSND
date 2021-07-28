import datetime

from settings import *


class Author(db.Model):
    __tablename__ = 'Author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # TODO: implement one-to-many relationship between Author and Book (DONE)
    books = db.relationship('Book', backref='author')

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'number_of_written_books': len(self.books),
        }


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)

    # TODO: implement one-to-many relationship between Category and Book (DONE)
    books = db.relationship('Book', backref='category')

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'number_of_books': len(self.books),
        }


class Book(db.Model):
    __tablename__ = 'Book'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    about = db.Column(db.String(255), nullable=False)

    author_id = db.Column('author_id', db.Integer, db.ForeignKey('Author.id', ondelete='CASCADE'),)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('Category.id', ondelete='CASCADE'),)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    # TODO: add rating here (Done)
    def get_rating(self):
        current_book_rating = 0
        for book in self.borrowed:
            ratings = BorrowedBooks.query.get(book.id)
            current_book_rating += ratings.rating
        avg_rating = current_book_rating / len(self.borrowed)
        return avg_rating

    def format(self):

        return {
            'id': self.id,
            'title': self.title,
            'pages': self.pages,
            'about': self.about,
            'number_of_borrowed_times': len(self.borrowed),
            'author': self.author.name,
            'category': self.category.title,
            'rating': f"{self.get_rating()} of 10",
        }


class Borrower(db.Model):
    __tablename__ = 'Borrower'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'number_of_borrowed_books': len(self.borrower),
        }


class BorrowedBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey('Book.id', ondelete='CASCADE'))
    borrower_id = db.Column('borrower_id', db.Integer, db.ForeignKey('Borrower.id', ondelete='CASCADE'))
    borrowed_at = db.Column(db.DateTime, default=datetime.datetime.now())

    # TODO: implement rating when a borrower returns a book (Done)
    returned_at = db.Column(db.DateTime)
    rating = db.Column(db.Float, default=0)

    borrower = db.relationship('Borrower', backref='borrower')
    borrowed = db.relationship('Book', backref='borrowed')

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'book': {
                'id': self.borrowed.id,
                'title': self.borrowed.title,
            },
            'borrowed_by': {
                'id': self.borrower.id,
                'name': self.borrower.name,
            },
            'borrowed_at': self.borrowed_at,
            'returned at': self.returned_at if self.returned_at is not None else "not returned yet",
            'rated': self.rating,
        }
