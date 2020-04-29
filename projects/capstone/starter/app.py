from flask import request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import create_app, setup_db, db_drop_and_create_all, Movie, Actor


database_path = "postgresql://postgres:password@localhost:5432/castingagency"


APP = create_app(database_path)
db = SQLAlchemy(APP)
database = setup_db(APP)
# db_drop_and_create_all()


@APP.route("/")
def index():
    movies = Movie.query.order_by(Movie.id)
    actors = Actor.query.order_by(Actor.id)
    movie_list = [movie.formatted() for movie in movies]
    actor_list = [actor.formatted() for actor in actors]

    return jsonify({
        "Movies": movie_list,
        "Actors": actor_list
    })


@APP.route("/actors", methods=['GET'])
def get_actors():
    actors = Actor.query.order_by(Actor.id)
    actor_list = [actor.formatted() for actor in actors]

    return jsonify({
        "Actors": actor_list
    })


@APP.route("/movies", methods=['GET'])
def get_movies():
    movies = Movie.query.order_by(Movie.id)
    movie_list = [movie.formatted() for movie in movies]

    return jsonify({
        "Movies": movie_list
    })


@APP.route("/actors/<int:actor_id>", methods=['GET'])
def get_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        return jsonify({
          "Actors": "No actors are currently present in the database."
        })
    else:
        return jsonify(actor.formatted())


@APP.route("/movies/<int:movie_id>", methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    return jsonify(movie.formatted())


@APP.route("/actors/<int:actor_id>", methods=['DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    actor.delete()

    return jsonify({
        "Actor": actor.name,
        "Deleted": True
    })


@APP.route("/movies/<int:movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    movie.delete()

    return jsonify({
        "Movie": movie.name,
        "Deleted": True
    })


@APP.route("/movies/create", methods=['POST'])
def add_movie():
    body = request.get_json()

    new_movie = Movie(body['title'], body['release_date'])
    new_movie.create()

    return jsonify(new_movie.formatted())


@APP.route("/actors/create", methods=['POST'])
def add_actor():
    body = request.get_json()

    new_actor = Actor(body['name'], body['age'], body['gender'])
    new_actor.create()

    return jsonify(new_actor.formatted())


@APP.route("/movies/<int:movie_id>", methods=['PATCH'])
def edit_movie(movie_id):
    body = request.get_json()

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    movie.title = body['title']
    movie.release_date = body['release_date']

    movie.update()

    return jsonify({
        "updated": True,
        "movie": movie.formatted()
    })


@APP.route("/actors/<int:actor_id>", methods=['PATCH'])
def edit_actor(actor_id):
    body = request.get_json()

    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    actor.name = body['name']
    actor.age = body['age']
    actor.gender = body['gender']

    actor.update()

    return jsonify({
        "updated": True,
        "actor": actor.formatted()
    })
# Default port:
# if __name__ == '__main__':
#     APP.run()

# Or specify port manually:
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 7000))
#     APP.run(host='localhost', port=port)
