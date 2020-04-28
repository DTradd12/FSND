import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all

database_path = "postgresql://postgres:password@localhost:5432/castingagency"


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    return app


APP = create_app()
db = SQLAlchemy(APP)
database = setup_db(APP)
db_drop_and_create_all()


# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)
