# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

import babel
import dateutil.parser
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify,
)
from flask_migrate import Migrate
from flask_moment import Moment

from forms import *
from models import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.app_context().push()
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
db.init_app(app)
db.create_all(app=app)


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
    cities = Venue.query.distinct(Venue.city, Venue.state).all()
    data = []
    for city in cities:
        data.append({
            'city': city.city,
            'state': city.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
            } for venue in Venue.query.all() if venue.city == city.city and venue.state == city.state
            ]
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. (Done)
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.ilike("%{0}%".format(search_term))).all()
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
    venue = Venue.query.get_or_404(venue_id)
    past_shows = Show.query.join(Artist).filter(Show.venue_id == venue_id). \
        filter(Show.start_time < datetime.now()).all()
    past_shows_count = len(past_shows)
    upcoming_shows = Show.query.join(Artist).filter(Show.venue_id == venue_id). \
        filter(Show.start_time > datetime.now()).all()
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
    form = VenueForm(request.form)

    # TODO: modify data to be the data object returned from db insertion

    try:
        venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
                      address=form.address.data, phone=form.phone.data,
                      facebook_link=form.facebook_link.data, image_link=form.image_link.data,
                      website_link=form.website_link.data, seeking_talent=form.seeking_talent.data,
                      seeking_description=form.seeking_description.data)
        genres = form.genres.data
        venue_genres = list()
        for genre in genres:
            temp_genre = Genre.query.filter_by(genre=genre).first()
            if temp_genre is None:
                db.session.add(Genre(genre=genre))
                db.session.commit()
            else:
                venue_genres.append(Genre.query.filter_by(genre=str(temp_genre)).first())
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
    data = Artist.query.filter(Artist.name.ilike("%{0}%".format(search_term))).all()
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
    artist = Artist.query.get_or_404(artist_id)
    past_shows = Show.query.join(Artist).filter(Show.venue_id == artist_id). \
        filter(Show.start_time < datetime.now()).all()
    past_shows_count = len(past_shows)
    upcoming_shows = Show.query.join(Artist).filter(Show.venue_id == artist_id). \
        filter(Show.start_time > datetime.now()).all()
    upcoming_shows_count = len(upcoming_shows)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
    }
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist = Artist.query.get_or_404(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website_link = form.website_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    genres = form.genres.data
    artist_genres = list()
    for genre in genres:
        if Genre.query.filter_by(genre=genre).first() is None:
            db.session.add(Genre(genre=genre))
            db.session.commit()
        else:
            artist_genres.append(Genre.query.filter_by(genre=genre).first())
    artist.genres = artist_genres
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    venue = Venue.query.get_or_404(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    genres = form.genres.data
    venue_genres = list()
    for genre in genres:
        if Genre.query.filter_by(genre=genre).first() is None:
            db.session.add(Genre(genre=genre))
            db.session.commit()
        else:
            venue_genres.append(Genre.query.filter_by(genre=str(genre)).first())
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
    form = ArtistForm(request.form)

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                        phone=form.phone.data, image_link=form.image_link.data,
                        facebook_link=form.facebook_link.data, website_link=form.website_link.data,
                        seeking_venue=form.seeking_venue.data, seeking_description=form.seeking_description.data)
        genres = form.genres.data
        artist_genres = list()
        for genre in genres:
            temp_genre = Genre.query.filter_by(genre=genre).first()
            if temp_genre is None:
                db.session.add(Genre(genre=genre))
                db.session.commit()
            else:
                artist_genres.append(Genre.query.filter_by(genre=genre).first())
        artist.genres = artist_genres
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + artist.name + ' was successfully listed!')
    except Exception as e:
        print(e)
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash('Artist ' + form.name.data + ' was not successfully listed!')
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
    data = Show.query.all()
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
    try:
        form = ShowForm(request.form)

        artist_id = form.artist_id.data
        venue_id = form.venue_id.data
        start_time = form.start_time.data

        venue = Venue.query.get_or_404(venue_id)
        show = Show(start_time=start_time)

        show.artist_id = artist_id
        show.venue_id = venue_id
        venue.shows.append(show)

        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show\'s data saved successfully!')
    except:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('there was an error saving the show\'s data!')
    finally:
        db.session.close()
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
