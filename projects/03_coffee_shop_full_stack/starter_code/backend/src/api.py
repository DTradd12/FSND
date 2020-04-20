import os
import json
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

APP = Flask(__name__)
setup_db(APP)
CORS(APP)


db_drop_and_create_all()


# ROUTES
@APP.route('/drinks', methods=['GET'])
def get_drinks():
    """Publicly gets all drinks from the database"""
    # Get all drinks from the database and format them.
    available_drinks = Drink.query.all()
    drinks = [drink.short() for drink in available_drinks]

    # Abort if no drinks exist.
    if len(drinks) == 0:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'drinks': drinks,
            'status_code': 200
        }), 200


@APP.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def drinks_detail(payload):
    """Privately gets all drinks from the database"""
    # Get all drinks from the database and format them.
    available_drinks = Drink.query.all()
    drinks = [drink.long() for drink in available_drinks]

    # Abort if there are no drinks.
    if len(available_drinks) == 0:
        abort(404)
    else:
        return jsonify({
            "success": True,
            "drinks": drinks,
            "status_code": 200
        }), 200


@APP.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def make_drink(payload):
    """Adds a new drink to the database"""
    # Get the submitted drink data and format it for submission.
    body = request.get_json()
    title = body["title"]
    recipe = body["recipe"]

    # Try to add a new drink to the database.
    try:
        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        new_drink.insert()

        return jsonify({
            "success": True,
            "drinks": new_drink.long(),
            "status_code": 200
        }), 200

    # On failure due to duplicate entry, abort 409.
    except exc.SQLAlchemyError:
        abort(409)


@APP.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def edit_drink(payload, drink_id):
    """Edits an existing drink in the database."""
    # Get the submitted drink data and format it for submission.
    body = request.get_json()
    new_title = body["title"]
    new_recipe = json.dumps(body["recipe"])

    # Search for the drink in the database.
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    # If the drink_id isn't in the database, abort.
    if not drink:
        abort(404)

    # Update the drink's data and submit it to the database.
    else:
        drink.title = new_title
        drink.recipe = new_recipe

        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()],
            "status_code": 200
        }), 200


@APP.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(payload, drink_id):
    """Deletes an existing drink from the database."""
    # Search for the drink in the database.
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    #  If the drink_id isn't in the database, abort.
    if not drink:
        abort(404)

    # If it is, delete it.
    elif drink.id == drink_id:
        drink.delete()

    return jsonify({
        "success": True,
        "delete": drink_id,
        "status_code": 200
    }), 200


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
        "error": error,
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
