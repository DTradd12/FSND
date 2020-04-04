from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    """Paginate a list of objects, in this case a list of questions."""
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the api
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # ROUTES
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        """Return all questions and all categories."""
        questions = Question.query.order_by(
            Question.id).all()  # Get all questions
        current_questions = paginate_questions(
            request, questions)  # Paginate the questions
        cats = Category.query.all()  # Get all categories
        categories = {}
        for cat in cats:
            # Format categories and add them to a dictionary
            categories.update({cat.id: cat.type})

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': None,
            'categories': categories
        })

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        """Returns all categories"""
        cats = Category.query.all()  # Get all categories
        categories = {}
        for cat in cats:
            # Format categories and add them to a dictionary
            categories.update({cat.id: cat.type})

        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """Delete a question by question_id."""
        question = Question.query.filter(
            Question.id == question_id).one_or_none()  # Search for the question with the question_id being sent.

        if question is None:
            abort(404)

        question.delete()  # Delete the question
        questions = Question.query.order_by(
            Question.id).all()  # Gather the remaining questions
        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        categories = [category.type for category in categories]

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': None,
            'categories': categories
        })

    @app.route('/questions', methods=['POST'])
    def add_question():
        """Add a new question to the database from the json submitted."""
        body = request.get_json()  # Get the submitted JSON data

        # Format the different submitted data.
        new_question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')
        searchTerm = body.get('searchTerm')

        new_question = Question(
            question=new_question, answer=answer, category=category, difficulty=difficulty)
        new_question.insert()  # Create and insert the new question.

        # Return all the questions, including the new one.
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(
            request, questions)  # Paginate
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        categories = [category.type for category in categories]

        return jsonify({
            'questions': current_questions,
            'total_questions': len(questions),
            'category': None,
            'categories': categories
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def question_by_category(category_id):
        """Filter questions by category."""
        questions = Question.query.filter_by(
            category=category_id)  # Get all categories, filtered by category_id
        # Format the question list.
        question_list = [question.format() for question in questions]

        return jsonify({
            "questions": question_list,
            "totalQuestions": len(question_list),
            "currentCategory": category_id
        })

    @app.route('/searchQuestions', methods=['POST'])
    def search_questions():
        """Search for questions by text in question."""
        body = request.get_json()  # Get submitted JSON body.
        search_term = body['searchTerm']  # Find search term from JSON.

        if len(search_term) == 0:  # If search term is blank, return all questions
            questions = Question.query.all()
            current_questions = [question.format() for question in questions]

        else:  # Filter questions by search term
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            current_questions = [question.format() for question in questions]

            if len(current_questions) == 0:  # If no questions like the search term, 404
                abort(404)

        cats = Category.query.all()
        categories = [category.format() for category in cats]

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': None,
            'categories': categories,
            'searchTerm': search_term
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """Set up the quiz portion of the game, return a randomly selected question based on the category selected (
        or not selected.) """
        body = request.get_json()

        # Get category_id form JSON
        quiz_category = int(body['quiz_category']['id'])
        # Get the previous questions from the quiz.
        previous_questions = body['previous_questions']
        category = Category.query.get(quiz_category)

        if quiz_category != 0:  # If quiz category is not 0, filter by id.
            # If any previous questions exist, search for questions not in that list.
            if len(previous_questions) > 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions),
                                                  Question.category == category.id).all()
            else:
                questions = Question.query.filter_by(
                    category=quiz_category).all()

        elif quiz_category == 0:  # If category is 0, return all questions.
            # If category is none, return all questions that aren't in previous q's.
            if len(previous_questions) > 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.all()

        elif category is None:
            abort(404)

        # If no questions remain that haven't been asked, 404.
        if len(questions) == 0:
            abort(404)
        else:  # Select a random question from the questions list and format it.
            currentQuestion = questions[random.randint(
                0, len(questions) - 1)].format()

        if len(questions) > 0:
            return jsonify({
                "success": True,
                "question": currentQuestion,
            })

        else:
            abort(404)

    # ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
