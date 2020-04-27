#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, or_
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), nullable=False, default=True)
    seeking_description = db.Column(db.String(120), nullable=True)
    created_at = db.Column(
        db.DateTime(), default=datetime.now(), nullable=False)
    show = db.relationship('Show', backref='venue')


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_perf = db.Column(db.Boolean(), nullable=False, default=True)
    seeking_description = db.Column(db.String(120), nullable=True)
    created_at = db.Column(
        db.DateTime(), default=datetime.now(), nullable=False)
    show = db.relationship('Show', backref='artist')


class Show(db.Model):
    __tablebame = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id'), nullable=False)
    start_time = db.Column(
        db.DateTime(), nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['GET'])
def index():
    artists = Artist.query.order_by(desc(Artist.created_at)).limit(10)
    venues = Venue.query.order_by(desc(Venue.created_at)).limit(10)
    return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    data = []
    for venue in venues:
        venues = []
        dataset = {
            "city": venue.city,
            "state": venue.state,
            "venues": venues
        }
        venue_name = Venue.query.filter_by(city=venue.city)
        for row in venue_name:
            venue = {"id": row.id, "name": row.name}
            if venue in venues:
                continue
            else:
                venues.append(venue.copy())
        if dataset in data:
            continue
        else:
            data.append(dataset)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '').lower()
    venues = Venue.query.filter(or_(func.lower(Venue.name).ilike(f"%{search_term}%"), func.lower(
        Venue.city).ilike(f"%{search_term}%"), func.lower(Venue.state).ilike(f"%{search_term}%"))).all()
    count = Venue.query.filter(or_(func.lower(Venue.name).ilike(f"%{search_term}%"), func.lower(
        Venue.city).ilike(f"%{search_term}%"), func.lower(Venue.state).ilike(f"%{search_term}%"))).count()
    responses = []
    for venue in venues:
        response = {
            "id": venue.id,
            "name": venue.name,
            "city": venue.city,
            "state": venue.state
        }
        responses.append(response.copy())
    return render_template('pages/search_venues.html', results=responses, count=count, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    shows = Show.query.all()
    past_shows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_show_count = 0
    for show in shows:
        if show.venue.id == venue_id:
            start_time = show.start_time.strftime("%m/%d/%y, %H:%M")
            now_time = datetime.now().strftime("%m/%d/%y, %H:%M")
            if start_time < now_time:
                past_shows_count += 1
                past_show = {
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": start_time
                }
                past_shows.append(past_show.copy())
            elif start_time > now_time:
                upcoming_show_count += 1
                upcoming_show = {
                    "artist_id": show.artist.id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": start_time
                }
                upcoming_shows.append(upcoming_show.copy())
    data = {
        "id": venue.id,
        "name":  venue.name,
        "genres": venue.genres,
        "city": venue.city,
        "state": venue.state,
        "address": venue.address,
        "phone": venue.phone,
        "website_link": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_show_count,
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
    try:
        form = VenueForm(request.form)
        form_data = f'{((form.name.data).strip()).lower()}, {((form.city.data).strip()).lower()}'
        venues = Venue.query.all()
        venue_data = []
        for venue in venues:
            venue_data.append(
                f'{venue.name.strip().lower()}, {venue.city.strip().lower()}')
        if form_data in venue_data:
            flash('That venue already exists!')
        else:
            if form.seeking_talent.data == 'True':
                seeking_talent = True
            else:
                seeking_talent = False
            newVenue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data, phone=form.phone.data, genres=form.genres.data,
                             image_link=form.image_link.data, facebook_link=form.facebook_link.data, seeking_talent=seeking_talent, seeking_description=form.seeking_description.data, website_link=form.website_link.data)
            db.session.add(newVenue)
            db.session.commit()
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
    except:
        flash('An error occurred. Venue ' +
              form.name.data + ' could not be listed.')
    home_artists = Artist.query.order_by(desc(Artist.created_at)).limit(10)
    home_venues = Venue.query.order_by(desc(Venue.created_at)).limit(10)
    return render_template('pages/home.html', venues=home_venues, artists=home_artists)


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.get(venue_id).delete()
        db.session.commit()
        flash('Venue successfully deleted!')
    except:
        flash('Delete unsuccessful. This venue still has a show/shows associated to it.')
    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = []
    for artist in artists:
        dataset = {
            "id": artist.id,
            "name": artist.name,
            "image_link": artist.image_link
        }
        data.append(dataset)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '').lower()
    artists = Artist.query.filter(or_(func.lower(Artist.name).ilike(f"%{search_term}%"), func.lower(
        Artist.city).ilike(f"%{search_term}%"), func.lower(Artist.state).ilike(f"%{search_term}%"))).all()
    count = Artist.query.filter(or_(func.lower(Artist.name).ilike(f"%{search_term}%"), func.lower(
        Artist.city).ilike(f"%{search_term}%"), func.lower(Artist.state).ilike(f"%{search_term}%"))).count()
    responses = []
    for artist in artists:
        response = {
            "id": artist.id,
            "name": artist.name,
            "city": artist.city,
            "state": artist.state
        }
        responses.append(response.copy())
    return render_template('pages/search_artists.html', results=responses, count=count, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    artist = Artist.query.get(artist_id)
    shows = Show.query.all()
    past_shows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_show_count = 0
    for show in shows:
        if show.artist.id == artist_id:
            show_time = show.start_time.strftime("%m/%d/%y, %H:%M")
            now_time = datetime.now().strftime("%m/%d/%y, %H:%M")
            if show_time < now_time:
                past_shows_count += 1
                past_show = {
                    "venue_id": show.venue.id,
                    "venue_name": show.venue.name,
                    "venue_image_link": show.venue.image_link,
                    "start_time": show_time
                }
                past_shows.append(past_show.copy())
            elif show_time > now_time:
                upcoming_show_count += 1
                upcoming_show = {
                    "venue_id": show.venue.id,
                    "venue_name": show.venue.name,
                    "venue_image_link": show.venue.image_link,
                    "start_time": show_time
                }
                upcoming_shows.append(upcoming_show.copy())
    data = {
        "id": artist.id,
        "name":  artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_perf": artist.seeking_perf,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_show_count,
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artists = Artist.query.filter(Artist.id == artist_id).all()
    for artist in artists:
        artist = {
            "id": artist.id,
            "name": artist.name
        }
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        form = ArtistForm(request.form)
        artist = Artist.query.get(artist_id)

        if form.seeking_perf.data == 'True':
            seeking_perf = True
        else:
            seeking_perf = False

        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_perf = seeking_perf
        artist.vseeking_description = form.seeking_description.data
        artist.website_link = form.website_link.data

        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully edited!')
    except:
        flash('An error occurred. Artist ' +
              form.name.data + ' could not be edited.')
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venues = Venue.query.filter(Venue.id == venue_id).all()
    for venue in venues:
        venue = {
            "id": venue.id,
            "name": venue.name
        }
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        form = VenueForm(request.form)
        venue = Venue.query.get(venue_id)

        if form.seeking_talent.data == 'True':
            seeking_talent = True
        else:
            seeking_talent = False

        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_perf = seeking_talent
        venue.vseeking_description = form.seeking_description.data
        venue.website_link = form.website_link.data

        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully edited!')
    except:
        flash('An error occurred. Venue ' +
              form.name.data + ' could not be edited.')
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
        form = ArtistForm(request.form)
        form_data = f'{((form.name.data).strip()).lower()}, {((form.city.data).strip()).lower()}'
        artists = Artist.query.all()
        artist_data = []

        for artist in artists:
            artist_data.append(
                f'{artist.name.strip().lower()}, {artist.city.strip().lower()}')

        if form_data in artist_data:
            flash('That artist already exists!')

        else:
            if form.seeking_perf.data == 'True':
                seeking_perf = True

            else:
                seeking_perf = False
            newArtist = Artist(name=form.name.data, city=form.city.data, state=form.state.data, phone=form.phone.data, genres=form.genres.data,
                               image_link=form.image_link.data, facebook_link=form.facebook_link.data, seeking_perf=seeking_perf, seeking_description=form.seeking_description.data, website_link=form.website_link.data)

            db.session.add(newArtist)
            db.session.commit()

            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' +
              form.name.data + ' could not be listed.')

    home_artists = Artist.query.order_by(desc(Artist.created_at)).limit(10)
    home_venues = Venue.query.order_by(desc(Venue.created_at)).limit(10)

    return render_template('pages/home.html', venues=home_venues, artists=home_artists)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = Show.query.all()
    data = []
    for show in shows:
        start_time = str(show.start_time)
        show = {
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": start_time
        }
        data.append(show.copy())
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm(request.form)
    artists = Artist.query.all()
    venues = Venue.query.all()
    artist_list = []
    venue_list = []

    for artist in artists:
        artist_list.append(artist.id)

    for venue in venues:
        venue_list.append(venue.id)

    if int(form.artist_id.data) in artist_list and int(form.venue_id.data) in venue_list:
        newShow = Show(artist_id=form.artist_id.data,
                       venue_id=form.venue_id.data, start_time=form.start_time.data)
        db.session.add(newShow)
        db.session.commit()

        # on successful db insert, flash success
        flash('Show was successfully listed!')

    elif int(form.artist_id.data) not in artist_list:
        flash('An error occurred. That artist_id does not exist.')

    elif int(form.venue_id.data) not in venue_list:
        flash('An error occurred. The show_id does not exist.')

    else:
        flash('An error occurred. Show could not be listed.')

    home_artists = Artist.query.order_by(desc(Artist.created_at)).limit(10)
    home_venues = Venue.query.order_by(desc(Venue.created_at)).limit(10)

    return render_template('pages/home.html', venues=home_venues, artists=home_artists)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
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
