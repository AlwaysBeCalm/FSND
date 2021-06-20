# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
db.create_all()

# ----------------------------------------------------------------------------#
# Association Tables.
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
    shows = db.relationship('Show')
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


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    cities = [city[0] for city in Venue.query.with_entities(Venue.city).all()]
    data = []
    for city in cities:
        data.append(Venue.query.filter(Venue.city == city).first())
    print(data)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (Done)
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.like("%{0}%".format(search_term))).all()
    result = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=result,
                           search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id (Done)
    # TODO: get the upcoming show (Done)
    venue = Venue.query.get(venue_id)
    past_shows = Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == venue.id).all()
    past_shows_count = len(past_shows)
    upcoming_shows = Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == venue.id).all()
    upcoming_shows_count = len(upcoming_shows)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
    }
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    form = request.form
    name = form.get('name', None)
    city = form.get('city', None)
    state = form.get('state', None)
    address = form.get('address', None)
    phone = form.get('phone', None)
    facebook_link = form.get('facebook_link', None)
    image_link = form.get('image_link', None)
    website_link = form.get('website_link', None)
    seeking_talent = True if form.get('seeking_talent', False) == 'y' else False
    seeking_description = form.get('seeking_description', None)
    genres = form.getlist('genres')

    # TODO: modify data to be the data object returned from db insertion

    try:
        venue = Venue(name=name, city=city, state=state, address=address,
                      phone=phone, facebook_link=facebook_link, image_link=image_link,
                      website_link=website_link, seeking_talent=seeking_talent,
                      seeking_description=seeking_description)
        venue_genres = list()
        for genre in genres:
            venue_genres.append(Genre.query.filter_by(genre=genre).first())
        venue.genres = venue_genres
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue\'s data saved successfully!')
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('there was an error saving the data!')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # TODO: SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail. (Done)
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False})
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage (Done)


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    data = Artist.query.filter(Artist.name.like("%{0}%".format(search_term))).all()
    result = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_artists.html', results=result,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    data = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = request.form
    artist = Artist.query.get(artist_id)
    artist.name = form.get('name', None)
    artist.city = form.get('city', None)
    artist.state = form.get('state', None)
    artist.phone = form.get('phone', None)
    artist.facebook_link = form.get('facebook_link', None)
    artist.image_link = form.get('image_link', None)
    artist.website_link = form.get('website_link', None)
    artist.seeking_venue = True if form.get('seeking_venue', False) == 'y' else False
    artist.seeking_description = form.get('seeking_description', None)
    genres = form.getlist('genres')
    artist_genres = list()
    for genre in genres:
        artist_genres.append(Genre.query.filter_by(genre=genre).first())
    artist.genres = artist_genres
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = request.form
    venue = Venue.query.get(venue_id)
    venue.name = form.get('name', None)
    venue.city = form.get('city', None)
    venue.state = form.get('state', None)
    venue.address = form.get('address', None)
    venue.phone = form.get('phone', None)
    venue.facebook_link = form.get('facebook_link', None)
    venue.image_link = form.get('image_link', None)
    venue.website_link = form.get('website_link', None)
    venue.seeking_talent = True if form.get('seeking_talent', False) == 'y' else False
    venue.seeking_description = form.get('seeking_description', None)
    genres = form.getlist('genres')
    venue_genres = list()
    for genre in genres:
        venue_genres.append(Genre.query.filter_by(genre=genre).first())
    venue.genres = venue_genres
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = request.form
    name = form.get('name', None)
    city = form.get('city', None)
    state = form.get('state', None)
    phone = form.get('phone', None)
    facebook_link = form.get('facebook_link', None)
    image_link = form.get('image_link', None)
    website_link = form.get('website_link', None)
    seeking_venue = True if form.get('seeking_venue', False) == 'y' else False
    seeking_description = form.get('seeking_description', None)
    genres = form.getlist('genres')

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        artist = Artist(name=name, city=city, state=state, phone=phone,
                        image_link=image_link, facebook_link=facebook_link,
                        website_link=website_link, seeking_venue=seeking_venue,
                        seeking_description=seeking_description)
        artist_genres = list()
        for genre in genres:
            artist_genres.append(Genre.query.filter_by(genre=genre).first())
        artist.genres = artist_genres
        print("got here")
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + artist.name + ' was successfully listed!')
    except Exception as e:
        print(e)
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash('Artist ' + name + ' was not successfully listed!')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
