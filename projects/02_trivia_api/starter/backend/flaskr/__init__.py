import os
from flask import Flask, request, abort, jsonify
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

# generate page of questions
# request -- request body 
# selection -- all questions
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_qs = questions[start:end]
  return current_qs

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      result = Category.query.all()
      categories = [category.type for category in result]
      return jsonify({
        'success': True,
        'categories': categories
      })
    except Exception as e:
      abort(400)

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    try:
      qs = Question.query.all()
      pageQs = paginate_questions(request, qs)
      categories = [cat.type for cat in Category.query.all()]
      return jsonify({
        'success': True,
        'questions': pageQs,
        'total_questions': len(qs),
        'categories': categories,
        'current_category': None
      })
    except:
      abort(404)

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.get(id)
      db.session.delete(question)
      db.session.commit()
    except:
      abort(422)
      db.session.rollback()
    finally:
      db.session.close()
    return "Deleted question with id: " + str(question.id)

  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.

  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      data = request.get_json()

      # check for searchTerm request vs adding new question
      if data.get('searchTerm'):
        search = data.get('searchTerm')
        response = Question.query.filter(func.lower(Question.question).like('%' + search + '%')).all()
        pageQs = paginate_questions(request, response)
        return jsonify({
          'success': True,
          'questions': pageQs,
          'total_questions': len(response),
          'currentCategory': None
        })

      else:
        category = int(data.get('category')) + 1 # bug with id indexing (categories DB start with 1, frontend start with 0)
        question = Question(question=data.get('question'), answer=data.get('answer'), category=category, difficulty=data.get('difficulty'))
        db.session.add(question)
        db.session.commit()
        return jsonify({
          'success': True,
          'question_id': question.id
        })

    except:
      abort(422)
      db.session.rollback()
    finally:
      db.session.close()

  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    try:
      category = Category.query.get(id+1) # bug with id indexing (categories DB start with 1, frontend start with 0)
      qs = Question.query.filter_by(category=category.id).all()
      pageQs = paginate_questions(request, qs)
      categories = [cat.type for cat in Category.query.all()]
      return jsonify({
        'success': True,
        'questions': pageQs,
        'total_questions': len(qs),
        'current_category': category.id
      })
    except:
      abort(404)

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      data = request.get_json()
      previous_qs = data['previous_questions']

      # gather all questions or questions within category
      if data['quiz_category']:
        category = int(data['quiz_category']['id']) + 1 # bug with id indexing (categories DB start with 1, frontend start with 0)
        questions = Question.query.filter_by(category=category).all()
      else:
        questions = Question.query.all()

      # get random question not already asked
      rand_question = questions[random.randint(0, len(questions)-1)]
      while rand_question.id in previous_qs:
        if len(previous_qs) == len(questions):
          rand_question = None
          break
        rand_question = questions[random.randint(0, len(questions)-1)]
      
      # can't format 'None' type
      if rand_question:
        rand_question = rand_question.format()
      
      return jsonify({
        'success': True,
        'question': rand_question,
      })

    except:
      abort(400)

  '''
  Create error handlers for all expected errors 
  including 400, 404, 422, and 500. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Server error"
    }), 500

  return app
