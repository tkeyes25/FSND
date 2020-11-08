# API Documentation

Here is where you will find the documentation in order to utilize the APIs in the trivia game.

## Getting Started

To get started, you will need to visit the [frontend README](frontend/README.md) and the [backend README](frontend/README.md) and follow the install instructions.

- APIs configured to port 3000

- Base URL
  - http://localhost:3000/
  - Will get the home page with all the paginated questions from the local database
  - There are no API keys or authentications necessary to utilize the APIs.

## Error Codes

- Response Body

```json
{
  "success": Boolean,
  "error": Integer,
  "message": String
}
```

- 400
  - Message: "Bad request"
  - type: json

- 404
  - Message: "Not found"
  - type: json

- 422
  - Message: "Unprocessable"
  - type: json

- 500
  - Message: "Server error"
  - type: json

## Resource Endpoint Library

- Questions
  - Load Questions
    - This endpoint should return a list of questions, number of total questions, current category, categories
    - Endpoint: /questions
    - Method: GET
    - Sample: http://localhost:3000questions
    - Response

    ```json
    {
      'success': Boolean,
      'questions': Array,
      'total_questions': Integer,
      'categories': Array
      'current_category': Integer
    }
    ```

  - Create Question
    - An endpoint to POST a new question,which will require the question and answer text, category, and difficulty score.
    - Endpoint: /questions
    - Method: POST
    - Sample: http://localhost:3000questions
    - Request Body

    ```json
    {
      question: String,
      answer: String,
      difficulty: Integer,
      category: Integer
    }
    ```

    - Response

    "Question created with id: {id}"

  - Search Questions
    - Get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
    - Endpoint: /questions
    - Method: POST
    - Sample: http://localhost:3000/questions
    - Request Body

    ```json
    {
      searchTerm: String
    }
    ```

    - Response

    ```json
    {
      'success': Boolean,
      'questions': Array,
      'total_questions': Integer,
      'currentCategory': Integer
    }

  - Delete Question
    - DELETE question using a question ID
    - Endpoint: /questions
    - Method: DELETE
    - Sample: http://localhost:3000/questions/<int:id>
    - Arguments
      - id **required**
        - Integer representing the unique id of the question to delete
    - Response

    "Deleted question with id: {id}"

- Categories
  - Load questions by category
    - Get questions based on category
    - Endpoint: /categories/<int:id>/questions
    - Method: GET
    - Sample: http://localhost:3000/categories/2/questions
    - Arguments
      - id **required**
        - Integer representing a preloaded category type
    - Response

    ```json
    {
      'success': True,
      'questions': pageQs,
      'total_questions': len(qs),
      'current_category': category.id
    }
    ```

- Quizzes
  - Play Quiz
    - get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
    - Endpoint: /quizzes
    - Method: GET
    - Sample: http://localhost:3000/quizzes
    - Request Body

    ```json
    {
      previous_questions: Array,
      quiz_category: Integer
    }
    ```

    - Response

    ```json
    {
      showAnswer: Boolean,
      previousQuestions: Array,
      currentQuestion: String,
      guess: String,
      forceEnd: Boolean
    }
    ```
