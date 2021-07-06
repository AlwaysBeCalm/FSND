import random

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Done
    ''' 
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"*": {"origins": '*'}})

    # Done
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    # Done
    ''' 
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories/', methods=['GET'])
    def categories():
        all_categories = {category.id: category.type for category in Category.query.all()}
        return jsonify({
            "categories": all_categories,
            "success": True,
        })

    # Done
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions/', methods=['GET'])
    def questions():

        page = request.args.get('page', 1, type=int)
        starting = (page - 1) * QUESTIONS_PER_PAGE
        ending = starting + QUESTIONS_PER_PAGE

        all_questions = Question.query.order_by(Question.id).all()
        formatted_questions = [question.format() for question in all_questions]
        current_questions = formatted_questions[starting:ending]
        number_of_questions = len(all_questions)

        all_categories = {category.id: category.type for category in Category.query.all()}
        return jsonify({
            "questions": current_questions,
            "current_category": "all",
            "categories": all_categories,
            "total_questions": number_of_questions,
            "success": True,
        })

    # Done
    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>/', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            try:
                question.delete()
                return jsonify(
                    {
                        "success": True,
                        "message": "Question deleted successfully."
                    }
                )
            except:
                abort(422)

    # Done
    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions/', methods=['POST'])
    def add_question():
        data = request.get_json()

        answer = data.get('answer', None)
        category = data.get('category', None)
        difficulty = data.get('difficulty', None)
        question = data.get('question', None)
        new_question = Question(answer=answer, category=category, difficulty=difficulty, question=question)
        try:
            new_question.insert()
            all_questions = [question.format() for question in Question.query.all()]
            return jsonify(
                {
                    "success": True,
                    "message": "Question saved successfully.",
                    "questions": all_questions,
                }
            )
        except:
            abort(422)

    # Done
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/questions/search/', methods=['POST'])
    def search_question():
        search_term = request.get_json().get('searchTerm', '')
        searched_questions = Question.query.filter(Question.question.ilike("%{}%".format(search_term))).all()
        total_questions = len(Question.query.all())
        return jsonify({
            "success": True,
            "questions": [question.format() for question in searched_questions],
            "total_questions": total_questions,
            "current_category": list(dict.fromkeys([question.category for question in searched_questions])),
        })

    # Done
    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions/', methods=['GET'])
    def get_questions_by_category(category_id):
        filtered_questions = Question.query.filter(Question.category == category_id).all()
        current_category = Category.query.get(category_id)
        if not current_category:
            abort(404)
        return jsonify({
            "success": True,
            "questions": [question.format() for question in filtered_questions],
            "total_questions": len(filtered_questions),
            "current_category": current_category.type,
        })

    # Done
    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes/', methods=['POST'])
    def play_the_quiz():
        data = request.get_json()
        quiz_type = data.get('quiz_category').get('type')
        if quiz_type != 'click':
            type_id = Category.query.filter(Category.type == quiz_type).one_or_none().id
            filtered_questions = Question.query.filter(Question.category == type_id).all()
        else:
            filtered_questions = Question.query.all()
        previous_questions = data.get('previous_questions')
        if previous_questions:
            filtered_questions = [question for question in filtered_questions if question.id not in previous_questions]
            if not filtered_questions:
                return jsonify({
                    "questions": None,
                })

        question = random.choice(filtered_questions)
        return jsonify({
            "success": True,
            "question": question.format(),
        })

    # Done
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "Message": "bad request",
            "error": 400,
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(
            {
                "Message": "forbidden",
                "error": 403,
            }
        ), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "Message": "Not Found.",
                "error": 404,
            }
        ), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "Message": "Method Not Allowed.",
                "error": 405,
            }
        ), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "Message": "Unprocessable.",
                "error": 422,
            }
        ), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify(
            {
                "Message": "Server Error.",
                "error": 500,
            }
        ), 500

    @app.errorhandler(502)
    def bad_gateway(error):
        return jsonify(
            {
                "Message": "bad gateway",
                "error": 502,
            }
        ), 502

    # WHEN HANDLING 3xx ERRORS, THE APPLICATION THROWS AN EXCEPTION.

    # @app.errorhandler(302)
    # def redirected(error):
    #     return jsonify({
    #         "Message": "redirected",
    #         "error": 302,
    #     }), 302

    # @app.errorhandler(304)
    # def not_modified(error):
    #     return jsonify({
    #         "Message": "not modified",
    #         "error": 304,
    #     }), 304

    return app
