#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://udacity:postgres@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(240))
    shows = db.relationship('Show', backref='venue_show_id')
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String())

    shows = db.relationship('Show', backref='artist_show_id')

class Show(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  venue = db.Column(db.Integer,db.ForeignKey("Venue.id"))
  artist = db.Column(db.Integer, db.ForeignKey("Artist.id"))
  show_date = db.Column(db.DateTime, default=datetime.utcnow)

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  now = now= datetime.utcnow()
  areas = db.session.query(Venue.city, Venue.state).group_by(Venue.city,Venue.state).all()
  for area in areas:
    v_data = []
    venues = Venue.query.filter(Venue.city == area.city).filter(Venue.state==area.state).all()
    
    for v in venues:
      upcoming_shows_count = 0
      # Upcoming shows not in template, so no reason to hinder performance for it
      '''for show in v.shows:
        if format_datetime(str(show.show_date)) > format_datetime(str(now)):
          upcoming_shows_count += 1'''
      v_data.append({
        "id": v.id,
        "name": v.name,
        "upcoming_shows_count": upcoming_shows_count
      })
    data.append({
      'city':area.city,
      'state':area.state,
      'venues': v_data
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={}
  response['count'] = 0
  response['data'] = []
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%"+ search_term +"%")).all()

  for venue in venues:
    upcoming_shows_count = 0
    now = now= datetime.utcnow()
    for show in venue.shows:
      if format_datetime(str(show.show_date)) > format_datetime(str(now)):
        upcoming_shows_count += 1
    response['data'].append({
      'id':venue.id,
      'name':venue.name,
      'num_upcoming_shows': upcoming_shows_count,
    })
    response['count'] += 1
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data = {}
  venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  now= datetime.utcnow()
  for show in venue.shows:
    if format_datetime(str(show.show_date)) > format_datetime(str(now)):
      upcoming_shows.append({
        "artist_id":show.artist,
        "artist_name":Artist.query.get(show.artist).name,
        "artist_image_link":Artist.query.get(show.artist).image_link,
        "start_time": format_datetime(str(show.show_date))
       })
    else:
      past_shows.append({
        "artist_id":show.artist,
        "artist_name":Artist.query.get(show.artist).name,
        "artist_image_link":Artist.query.get(show.artist).image_link,
        "start_time": format_datetime(str(show.show_date))
       })
    past_shows_count = len(past_shows)
    upcoming_shows_count = len(upcoming_shows)
    
    data['upcoming_shows']= upcoming_shows
    data['past_shows'] = past_shows
    data['upcoming_shows_count'] = upcoming_shows_count
    data['past_shows_count'] = past_shows_count
    
  return render_template('pages/show_venue.html', data=data, venue=venue)
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  city = request.form.get('city')
  state = state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone','')
  image_link = request.form.get('image_link', '')
  facebook_link = request.form.get('facebook_link', '')
  seeking_talent = True if request.form.get('seeking_talent') == 'y' else False 
  seeking_description = request.form.get('seeking_description','')
  try:
    new_venue = Venue(
      name=name, city=city, state=state, address=address,phone=phone, image_link=image_link, 
      facebook_link=facebook_link, seeking_talent=seeking_talent,seeking_description=seeking_description
      )
    db.session.add(new_venue)
    db.session.commit()
     # on successful db insert, flash success
    flash('Venue ' + name + ' was successfully listed!')
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  finally:
    db.session.close()
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data= Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={}
  response['count'] = 0
  response['data'] = []
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%"+ search_term +"%")).all()

  for artist in artists:
    upcoming_shows_count = 0
    now = now= datetime.utcnow()
    for show in artist.shows:
      if format_datetime(str(show.show_date)) > format_datetime(str(now)):
        upcoming_shows_count += 1
    response['data'].append({
      'id':artist.id,
      'name':artist.name,
      'num_upcoming_shows': upcoming_shows_count,
    })
    response['count'] += 1
  
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  data = {}
  artist = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  now= datetime.utcnow()
  for show in artist.shows:
    if format_datetime(str(show.show_date)) > format_datetime(str(now)):
      upcoming_shows.append({
        "venue_id":show.venue,
        "venue_name":Venue.query.get(show.venue).name,
        "venue_image_link":Venue.query.get(show.venue).image_link,
        "start_time": format_datetime(str(show.show_date))
       })
    else:
      past_shows.append({
        "venue_id":show.venue,
        "venue_name":Venue.query.get(show.venue).name,
        "venue_image_link":Venue.query.get(show.venue).image_link,
        "start_time": format_datetime(str(show.show_date))
       })
    past_shows_count = len(past_shows)
    upcoming_shows_count = len(upcoming_shows)
    data['upcoming_shows']= upcoming_shows
    data['past_shows'] = past_shows
    data['upcoming_shows_count'] = upcoming_shows_count
    data['past_shows_count'] = past_shows_count
    
  return render_template('pages/show_artist.html', data=data, artist = artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  name = request.form.get('name','')
  city = request.form.get('city','')
  state = request.form.get('state','')
  phone = request.form.get('phone','')
  genres = request.form.getlist('genres')
  facebook_link = request.form.get('facebook_link','')
  image_link = request.form.get('image_link','')
  seeking_venue = request.form.get('seeking_venue')
  seeking_description = request.form.get('seeking_description','')

  try:
    artist.name = name
    artist.city = city
    artist.state = state
    artist.phone = artist.phone if phone == '' else phone
    artist.genres = artist.genres if genres == '' else genres
    artist.facebook_link = artist.facebook_link if facebook_link == '' else facebook_link
    artist.image_link = artist.image_link if image_link == '' else image_link
    artist.seeking_venue = True if seeking_venue == 'y' else False
    artist.seeking_description = artist.seeking_description if seeking_description == '' else seeking_description
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + name + ' was successfully updated!')

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + name + ' could not be updated.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue= Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)

  name = request.form.get('name')
  city = request.form.get('city')
  state = state = request.form.get('state')
  address = request.form.get('address','')
  phone = request.form.get('phone','')
  image_link = request.form.get('image_link', '')
  facebook_link = request.form.get('facebook_link', '')
  seeking_talent = True if request.form.get('seeking_talent') == 'y' else False 
  seeking_description = request.form.get('seeking_description','')

  try:
    venue.name = name
    venue.city = city
    venue.state = state
    venue.address = address
    venue.phone = venue.phone if phone == '' else phone
    venue.image_link = venue.image_link if image_link == '' else image_link
    venue.facebook_link = venue.facebook_link if facebook_link == '' else facebook_link
    venue.seeking_talent = seeking_talent
    venue.seeking_description = venue.seeking_description if seeking_description == '' else seeking_description
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + name + ' was successfully updated!')

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + name + ' could not be updated.')

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
  # TODO: insert form data as a new Artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone', '')
  image_link = request.form.get('image_link', '')
  genres = request.form.get('genres', '')
  facebook_link = request.form.get('facebook_link', '')
  seeking_venue = True if request.form.get('seeking_venue') == 'y' else False 
  seeking_description = request.form.get('seeking_description','')

  
  try:
    new_artist = Artist(
      name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, 
      seeking_venue = seeking_venue, seeking_description=seeking_description
      )
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + new_artist.name + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  shows = Show.query.all()
  for show in shows:
    data.append({
      "venue_id": show.venue,
      "venue_name": Venue.query.get(show.venue).name,
      "artist_id" : show.artist,
      "artist_name" : Artist.query.get(show.artist).name,
      "artist_image_link" : Artist.query.get(show.artist).image_link,
      "start_time" : format_datetime(str(show.show_date))
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
  # TODO: insert form data as a new Show record in the db, instead
  venue_id = request.form.get("venue_id")
  artist_id = request.form.get("artist_id")
  start_time = request.form.get("start_time")
  # on successful db insert, flash success
  try:
    show = Show(venue=venue_id,artist=artist_id,show_date=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
