import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .auth.auth import requires_auth
from .database.models import setup_db, Drink

app = Flask(__name__)
setup_db(app)
CORS(app)

''' (DONE)
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
# db_drop_and_create_all()

# ROUTES
''' (DONE)
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/', methods=['GET'])
@requires_auth('public')
def get_drinks():
    all_drinks = Drink.query.all()
    drinks = [drink.short() for drink in all_drinks]
    return jsonify({
        'success': True,
        'drinks': drinks,
    }), 200


''' (DONE)
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details():
    all_drinks = Drink.query.all()
    drinks = [drink.long() for drink in all_drinks]
    return jsonify({
        'success': True,
        'drinks': drinks,
    }), 200


''' (DONE)
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    data = request.get_json()
    new_drink = Drink()
    new_drink.title = data.get('title', None)
    new_drink.recipe = json.dumps(data.get('recipe', None))
    try:
        new_drink.insert()
        return jsonify({
            'success': True,
            'drinks': new_drink.long(),
        }), 200
    except:
        abort(422)


''' (DONE)
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)

    data = request.get_json()
    drink.title = data.get('title', drink.title)
    drink.recipe = json.dumps(data.get('recipe', drink.recipe))
    try:
        drink.update()
        return jsonify({
            'success': True,
            'drink': drink.long(),
        }), 200
    except:
        abort(422)


''' (DONE)
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id,
        }), 200
    except:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable."
    }), 422


''' (DONE)
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request."
    }), 400


@app.errorhandler(401)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized."
    }), 401


''' (DONE)
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(403)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "unauthorized."
    }), 403


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found."
    }), 404


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server Error."
    }), 500


''' NOTE: THE AuthError ERROR AND EXCEPTIONS IS IMPLEMENTED ON auth.py
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
