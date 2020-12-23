#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, \
                    url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from tempfile import mkdtemp
from flask_session import Session

import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

moment = Moment(app)
#Connect to SQL database -> config.py
app.config.from_object('config')
#Filesystem session instead of signed cookies
Session(app)
#Instance of SQLAlchemy
db = SQLAlchemy(app)
#Initialize Flask Migrate
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
#Many to many relationships

class Venue(db.Model):
    __tablename__ = "venues"
    #Own data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(5), default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    #Debugging print out formatting
    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = "artists"
    #Own data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(5), default=False)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    #Debugging print out formatting
    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    #Own data
    start_time = db.Column(db.DateTime(), nullable=False)
    #Foreign key with cascading delete
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id',
                        ondelete='CASCADE'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id',
                        ondelete="CASCADE"), nullable=False)
    #Relationships with cascading delete
    venues = db.relationship('Venue', backref=db.backref('shows',
        cascade='all,delete'), lazy='select')
    artists = db.relationship('Artist', backref=db.backref('shows',
        cascade='all,delete'), lazy='select')
    #Debugging print out formatting
    def __repr__(self):
        return f'<Show {self.id} {self.venue_id} {self.artist_id}>'

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
#Jinja Filter, called with "|"
app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

# -----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------
"""Venues overview"""
@app.route('/venues')
def venues():
    #Venues overview list, grouped by same locations and unique -> distinct
    data = []
    #Get all city/state combinations, unique -> distinct
    city_state = db.session.query(Venue.city, Venue.state) \
        .distinct(Venue.city, Venue.state)
    #Loop trough city/state list and combine venues in a list data at same location
    #Dict structure of each list item necessary for html front end
    for loc in city_state:
        same_loc = db.session.query(Venue.id, Venue.name).order_by(Venue.name) \
            .filter(Venue.city == loc[0]) \
            .filter(Venue.state == loc[1])
        data.append({
            "city" : loc[0],
            "state" : loc[1],
            "venues" : same_loc
        })

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

"""Venue detail page"""
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # HTML needs dict
    data = {}
    venue = Venue.query.filter_by(id=venue_id).one()

    #Add past and upcoming shows
    shows = Show.query.filter_by(venue_id=venue_id).all()
    upcoming_shows = []
    past_shows = []
    now = datetime.now()

    for show in shows:
        temp = {
            "artist_image_link" : show.artists.image_link,
            "artist_id" : show.artist_id,
            "artist_name" : show.artists.name,
            "start_time" : show.start_time.strftime("%Y-%m-%d %H:%M")
        }
        #Check if upcoming or past
        if show.start_time < now:
            past_shows.append(temp)
        else:
            upcoming_shows.append(temp)

    data={
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        }

    data["upcoming_shows_count"] = len(upcoming_shows)
    data["past_shows_count"] = len(past_shows)

    data["upcoming_shows"] = upcoming_shows
    data["past_shows"] = past_shows

    return render_template('pages/show_venue.html', venue=data)

"""Create Venue"""
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    try:
        #Get user input form data from HTML
        form = VenueForm(request.form)
        #Duplicate check, if name is already ecisiting in db -> skip
        name = form.name.data
        #Ensure duplicate checks, even if db has already duplicates -> all()[0]
        try:
            db_name = Venue.query.filter_by(name=name).all()[0]
            if db_name.name == name:
                flash('Venue ' + request.form['name'] + ' already exists!')
        except:
            venue = Venue(
                name = form.name.data,
                city = form.city.data,
                state = form.state.data,
                address = form.address.data,
                phone = form.phone.data,
                website = form.website.data,
                image_link = form.image_link.data,
                facebook_link = form.facebook_link.data,
                seeking_talent = form.seeking_talent.data,
                seeking_description = form.seeking_description.data,
                genres = form.genres.data
            )

            db.session.add(venue)
            db.session.commit()
            # on successful db insert, flash success
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        #on unsuccessful db insert, flash an error instead.
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')

"""Delete Venue"""
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        #Cascading delete implemented in Model (Foreign Key and Relationships)
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue has been DELETED!')
    except:
        db.session.rollback()
        flash('Error: Venue was NOT deleted!')
    finally:
        db.session.close()

    return redirect("/")

#  Artists
#  ----------------------------------------------------------------
"""Artists overview"""
@app.route('/artists')
def artists():
    #Artists overview list, each artist is unique, no grouping as Venues
    data = Artist.query.order_by('id').all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

"""Artist detail page"""
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # HTML needs dict
    data = {}
    artist = Artist.query.filter_by(id=artist_id).one()

    #Add past and upcoming shows
    shows = Show.query.filter_by(artist_id=artist_id).all()
    upcoming_shows = []
    past_shows = []
    now = datetime.now()

    for show in shows:
        temp = {
            "venue_image_link" : show.venues.image_link,
            "venue_id" : show.venue_id,
            "venue_name" : show.venues.name,
            "start_time" : show.start_time.strftime("%Y-%m-%d %H:%M")
        }

        if show.start_time < now:
            past_shows.append(temp)
        else:
            upcoming_shows.append(temp)

    data={
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link
    }

    data["upcoming_shows_count"] = len(upcoming_shows)
    data["past_shows_count"] = len(past_shows)

    data["upcoming_shows"] = upcoming_shows
    data["past_shows"] = past_shows

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

"""Create Artist"""
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    try:
        #Get user input form data from HTML
        form = ArtistForm(request.form)
        #Duplicate check, if name is already ecisiting in db -> skip
        name = form.name.data
        #Ensure duplicate checks, even if db has already duplicates -> all()[0]
        try:
            db_name = Artist.query.filter_by(name=name).all()[0]
            if db_name.name == name:
                flash('Artist ' + request.form['name'] + ' already exists!')
        except:
            artist = Artist(
                name = form.name.data,
                city = form.city.data,
                state = form.state.data,
                phone = form.phone.data,
                website = form.website.data,
                image_link = form.image_link.data,
                facebook_link = form.facebook_link.data,
                seeking_venue = form.seeking_venue.data,
                seeking_description = form.seeking_description.data,
                genres = form.genres.data,
            )

            db.session.add(artist)
            db.session.commit()
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
"""Shows overview"""
@app.route('/shows')
def shows():
    # displays list of shows at /shows, chronological sorted
    shows = Show.query.order_by('start_time').all()
    #Create data list with joined data from Artist and Venue table
    data = []
    for show in shows:
        #Append dict, as needed by HTML
        data.append({
            "artist_image_link" : show.artists.image_link,
            "start_time" : show.start_time.strftime("%Y-%m-%d %H:%M"),
            "artist_id" : show.artist_id,
            "artist_name" : show.artists.name,
            "venue_id" : show.venue_id,
            "venue_name" : show.venues.name
        })


    datas=[{
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

"""Create Show"""
@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    try:
        form = ShowForm(request.form)

        show = Show(
            artist_id = form.artist_id.data,
            venue_id = form.venue_id.data,
            start_time = form.start_time.data
        )

        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
