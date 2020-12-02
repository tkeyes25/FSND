import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(payload):
    try:
        drinks = []
        for drink in Drink.query.all():
            drinks.append(drink.short())
        return jsonify({
            "success": True,
            "drinks": drinks
        })
    except:
        abort(400)

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = []
        for drink in Drink.query.all():
            drinks.append(drink.long())
        return jsonify({
            "success": True,
            "drinks": drinks
        })
    except:
        abort(400)

'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        data = request.get_json()
        title = data.get('title', None)
        recipe = data.get('recipe', None)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        drink = Drink.query.filter(Drink.title == title).one_or_none()
        drink = drink.long()
        return jsonify({
            'success': True,
            'drinks': drink
        })
    except:
        abort(400)
'''
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
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(payload, id):
    try:
        data = request.get_json()
        drink = Drink.query.get(id)
        drink.title = data.get('title', None)
        drink.recipe = json.dumps(data.get('recipe', None))
        drink.update()
        drink = [drink.long()]
        return jsonify({
            "success": True,
            "drinks": drink
        })
    except:
        abort(404)
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('get:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.get(id)
        # drink.delete()
        return jsonify({
            "success": True,
            "drinks": drink
        })
    except Exception as e:
        print(e)
        abort(404)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
implement error handler for 404
    error handler should conform to general task above 
'''

# @app.errorhandler(404)
# def unprocessable(error):
#     return jsonify({
#         "success": False, 
#         "error": 404,
#         "message": "resource not found"
#     }), 404

# '''
# implement error handler for AuthError
#     error handler should conform to general task above 
# '''

# @app.errorhandler(AuthError)
# def unauthorized(error):
#     return jsonify({
#         "success": False, 
#         "error": 401,
#         "message": "unauthorized"
#     }), 401