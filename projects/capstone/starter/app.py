from flask import request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from .database.models import create_app, setup_db, db_drop_and_create_all, Movie, Actor
from .auth.auth import AuthError, requires_auth


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
        "success": True,
        "status_code": 200,
        "movies": movie_list,
        "actors": actor_list
    })


@APP.route("/actors", methods=['GET'])
@requires_auth(permission='get:actors')
def get_actors():
    actors = Actor.query.order_by(Actor.id)
    actor_list = [actor.formatted() for actor in actors]

    if len(actor_list) == 0:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "status_code": 200,
            "actors": actor_list
        })


@APP.route("/movies", methods=['GET'])
@requires_auth(permission='get:movies')
def get_movies():
    movies = Movie.query.order_by(Movie.id)
    movie_list = [movie.formatted() for movie in movies]

    if len(movie_list) == 0:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "status_code": 200,
            "movies": movie_list
        })


@APP.route("/actors/<int:actor_id>", methods=['GET'])
@requires_auth(permission='get:actors')
def get_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "status_code": 200,
            "actor": actor.formatted()
        })


@APP.route("/movies/<int:movie_id>", methods=['GET'])
@requires_auth(permission='get:movies')
def get_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "status_code": 200,
            "movie": movie.formatted()
        })


@APP.route("/actors/<int:actor_id>", methods=['DELETE'])
@requires_auth(permission='delete:actor')
def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    actor.delete()

    if not actor:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "status_code": 200,
            "deleted": actor.id
        })


@APP.route("/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth(permission='delete:movie')
def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    movie.delete()

    if not movie:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "status_code": 200,
            "deleted": movie.id
        })


@APP.route("/movies/create", methods=['POST'])
@requires_auth(permission='post:movie')
def add_movie():
    body = request.get_json()

    try:
        new_movie = Movie(body['title'], body['release_date'])
        new_movie.create()

        return jsonify({
            "success": True,
            "status_code": 200,
            "movie": new_movie.formatted()
        })
    except exc.SQLAlchemyError:
        abort(409)
    

@APP.route("/actors/create", methods=['POST'])
@requires_auth(permission='post:actor')
def add_actor():
    body = request.get_json()

    try:
        new_actor = Actor(body['name'], body['age'], body['gender'])
        new_actor.create()
    
        return jsonify({
            "success": True,
            "status_code": 200,
            "actor": new_actor.formatted()
        })
    except exc.SQLAlchemyError:
        abort(409)


@APP.route("/movies/<int:movie_id>", methods=['PATCH'])
@requires_auth(permission='edit:movie')
def edit_movie(movie_id):
    body = request.get_json()

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if not movie:
        abort(404)
    else:
        movie.title = body['title']
        movie.release_date = body['release_date']

        movie.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "movie": movie.formatted()
        })


@APP.route("/actors/<int:actor_id>", methods=['PATCH'])
@requires_auth(permission='edit:actor')
def edit_actor(actor_id):
    body = request.get_json()

    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if not actor:
        abort(404)
    else:
        actor.name = body['name']
        actor.age = body['age']
        actor.gender = body['gender']

        actor.update()

        return jsonify({
            "success": True,
            "status_code": 200,
            "actor": actor.formatted()
        })


# Error Handling
@APP.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code


@APP.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@APP.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@APP.errorhandler(409)
def duplicate_entry(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "duplicate of an existing entry"
    }), 409


@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

# Default port:
# if __name__ == '__main__':
#     APP.run()

# Or specify port manually:
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 7000))
#     APP.run(host='localhost', port=port)
