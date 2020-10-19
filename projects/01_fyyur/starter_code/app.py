#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    upcoming_shows = db.relationship("Show")
    past_shows = db.relationship("Show")

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    upcoming_shows = db.relationship("Show")
    past_shows = db.relationship("Show")

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(120))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))

#----------------------------------------------------------------------------#
# Helper Functions.
#----------------------------------------------------------------------------#

# Calculate the upcoming and past shows for venue and artists
def past_upcoming_shows(id, model):
  query_results = []
  previous = []
  upcoming = []
  if model == "venue":
    query_results = Show.query.filter_by(venue_id=id).all()
  elif model == "artist":
    query_results = Show.query.filter_by(artist_id=id).all()
  for show in query_results:
    show_time = datetime.strptime(show.start_time, '%Y-%m-%d %H:%M:%S')
    if show_time < datetime.now():
      previous.append(show)
    else:
      upcoming.append(show)
  return previous, upcoming

# Get shows for a venue or artist
def get_shows_info(shows, model):
  for show in shows:
    if model == "venue":
      artist = Artist.query.get(show.artist_id)
      show.artist_name = artist.name
      show.artist_image_link = artist.image_link
    elif model == "artist":
      venue = Venue.query.get(show.venue_id)
      show.venue_name = venue.name
      show.venue_image_link = venue.image_link

# For WTF BoolienField Form and saving to DB
def boolean_field(bool_field):
  if bool_field == 'y':
    return True
  else:
    return False

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  result = Venue.query.all()
  data = []
  for venue in result:
    data.append({
      "city": venue.city, 
      "state": venue.state, 
      "venues": [{
        "id": venue.id,
        "name": venue.name
      }]
     })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # search on artists with partial string search. Ensure it is case-insensitive.
  search = request.form.get('search_term', '').lower()
  response = Venue.query.filter(func.lower(Venue.name).like('%' + search + '%')).all()
  return render_template('pages/search_venues.html', results=response, search_term=search)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data = Venue.query.get(venue_id)
  past, upcoming = past_upcoming_shows(venue_id, "venue")
  data.past_shows = past
  data.past_shows_count = len(past)
  data.upcoming_shows = upcoming
  data.upcoming_shows_count = len(upcoming)
  get_shows_info(data.past_shows, "venue")
  get_shows_info(data.upcoming_shows, "venue")

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  try:
    data = request.form.to_dict()
    venue = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'], phone=data['phone'], image_link=data['image_link'], facebook_link=data['facebook_link'], website=data['website'], seeking_talent=data['seeking_talent'], seeking_description=data['seeking_description'])
    venue.seeking_talent = boolean_field(venue.seeking_talent)
    db.session.add(venue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + venue.name + ' was successfully listed!')

  except:
    # on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
  if error:
    abort(500)

  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  result = Artist.query.all()
  data = []
  for artist in result:
    data.append({"id": artist.id, "name": artist.name})

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # search on artists with partial string search. Ensure it is case-insensitive.
  search = request.form.get('search_term', '').lower()
  response = Artist.query.filter(func.lower(Artist.name).like('%' + search + '%')).all()
  return render_template('pages/search_artists.html', results=response, search_term=search)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  data = Artist.query.get(artist_id)
  past, upcoming = past_upcoming_shows(artist_id, "artist")
  data.past_shows = past
  data.past_shows_count = len(past)
  data.upcoming_shows = upcoming
  data.upcoming_shows_count = len(upcoming)
  get_shows_info(data.past_shows, "artist")
  get_shows_info(data.upcoming_shows, "artist")
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = Artist.query.get(artist_id)
    data = request.form.to_dict()
    result = Artist(name=data['name'], city=data['city'], state=data['state'], phone=data['phone'], genres=data['genres'], image_link=data['image_link'], facebook_link=data['facebook_link'], website=data['website'], seeking_venue=data['seeking_venue'], seeking_description=data['seeking_description'])
    artist.name = result.name
    artist.city = result.city
    artist.state = result.state
    artist.phone = result.phone
    artist.genres = result.genres
    artist.image_link = result.image_link
    artist.facebook_link = result.facebook_link
    artist.website = result.website
    artist.seeking_venue = result.seeking_venue
    artist.seeking_description = result.seeking_description
    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Artist.query.get(venue_id)
    data = request.form.to_dict()
    result = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'], phone=data['phone'], image_link=data['image_link'], facebook_link=data['facebook_link'], website=data['website'], seeking_talent=data['seeking_talent'], seeking_description=data['seeking_description'])
    venue.name = result.name
    venue.city = result.city
    venue.state = result.state
    venue.phone = result.phone
    venue.address = result.address
    venue.image_link = result.image_link
    venue.facebook_link = result.facebook_link
    venue.website = result.website
    venue.seeking_talent = result.seeking_talent
    venue.seeking_description = result.seeking_description
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
  finally:
    db.session.close()
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
  try:
    data = request.form.to_dict()
    artist = Artist(name=data['name'], city=data['city'], state=data['state'], phone=data['phone'], genres=data['genres'], image_link=data['image_link'], facebook_link=data['facebook_link'], website=data['website'], seeking_venue=data['seeking_venue'], seeking_description=data['seeking_description'])
    artist.seeking_venue = boolean_field(artist.seeking_venue)
    db.session.add(artist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + artist.name + ' was successfully listed!')

  except:
    # on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    db.session.rollback()
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')

  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  result = Show.query.all()
  data = []
  for show in result:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    data.append({
      "venue_id": show.venue_id, 
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  try:
    data = request.form.to_dict()
    show = Show(artist_id=data['artist_id'], venue_id=data['venue_id'], start_time=data['start_time'])
    db.session.add(show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except():
    # on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  finally:
    db.session.close()
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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
