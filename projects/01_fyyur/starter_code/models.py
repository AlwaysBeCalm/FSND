from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------------------------------------------#
# Association Tables.
# These tables is to implements 3NF for the schema as every venue can be assigned
# many genres, and a genre can be assigned to many venues, and the same for artists
# ----------------------------------------------------------------------------#
venue_genre = db.Table('venue_genre',
                       db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id', ondelete='CASCADE')),
                       db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE')),
                       )

artist_genre = db.Table('artist_genre',
                        db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id', ondelete='CASCADE')),
                        db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE')),
                        )


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.genre}"


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (Done)
    shows = db.relationship('Show', backref=db.backref('venue'), lazy="joined")
    genres = db.relationship("Genre", uselist=True, secondary=venue_genre)
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.id}: {self.name}"


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate (Done)
    shows = db.relationship('Show', backref=db.backref('artist'), lazy="joined")
    genres = db.relationship("Genre", uselist=True, secondary=artist_genre)
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.id}: {self.name}"


# TODO Implement Show and Artist models, and complete all model relationships and properties,
#  as a database migration. (Done)

class Show(db.Model):
    artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), primary_key=True)
    venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), primary_key=True)
    start_time = db.Column('start_time', db.DateTime, primary_key=True)
    child = db.relationship('Venue')
