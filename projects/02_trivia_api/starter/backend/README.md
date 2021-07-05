# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## Endpoints docs
```
GET /categories/
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: an object with a single key, categories, that contains an object of id: category as key:value pair
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}


GET /questions/
- Fetches a dictionary of all the questions paginated 10 questions per page
- Request Arguments: page, which indicate the number of the current page
- Returns: 
    1- an object questions, contains all the question per current page.
    2- an object current_category, which in this case indicates 'all', not a specific one.
    3- a dictionary of categories as id: category in key:value pair format
    4- an object total_questions, which indicates the total questions in the table.


DELETE /questions/<int:question_id>/
- Delete a specific question from the database
- Request Arguments: question_id, which indicate the id of the question which will be deleted.
- Returns:
    1- a message that indicate a successfull deletion of a question.
    2- or return a 404 error if the requested question doesn't exist


POST /questions/
- Creates a new question, and save it in the database
- Requested Arguments: 1- the question text, 2- the answer text, 3- the category number, 4- and finally the difficulty number...
- Returns: 
    1- an object which contains all the questions, and successfull saving message
    2- or return an 422 error in case of failing in processing/saving the question.


POST /questions/search/
- Fetches the questions which contains the search term
- Requested Arguments: the searchTerm text
- Returns:
    1- an object questions, which contains all the searched questions.
    2- an object total_questions, which indicates the total of all the questions in the database
    3- an object current_category, which indicates the categories of the searched questions


GET /categories/<int:category_id>/questions/
- Fetches the question of a specific category
- Requested Arguments: the categrory_id number
- Returns:
    1- an object questions, which contains all the questions of a specific category
    2- an object total_questions, which indicates the total questions in a specific category
    3- an object current_category, which is the type of the passed category_id


POST /quizzes/
- Fetches all the questions or questions of a specific category from the database
- Requested Arguments: 1- the type of the quiz_category, 2- the previous_questions list
- Return: an object question which is a random question of all the questions or of a specific category from the database
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
