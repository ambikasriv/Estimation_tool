from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils import *
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'name_ambika'
client = MongoClient("mongodb://localhost:27017/")
db = client['Capstone'] # creating database here
user_collection = db['User'] # defining / creating User collection
historical_collection = db['Estimation']
bcrypt = Bcrypt(app)



@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/register', methods=['GET','POST'])
def register():
    """
    This function handles user registration requests.
    - It will render the registration form template (if implemented) through Get method.
    - and processes user registration data submitted through the form.
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data['name'] or not data['email'] or not data['contact'] or not data['password']:
            return jsonify({'error':"All fields input required"}), 400
        print(data)
        name = data['name']
        email = data['email']
        contact = data['contact']
        password = data['password']
        user_data ={
            'name' : name,
            'email' : email,
            'contact' : contact,
            'password' : password
        }

        if user_collection.find_one({'email': email}):
            return jsonify({"error": "User already exists"}), 401

        user_collection.insert_one(data)
        return jsonify({"message": "User registered successfully"}), 201
    return render_template('registration.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    """it handles user login requests.

    - Processes login data sent in a POST request, validates email and password presence,checks if user exists with the provided email in the database (user_collection).
    - Verifies password if user is found, generates an access token on successful login using JWT.
    - Returns appropriate responses based on login success or failure, renders the login_page.html template for GET requests.
    """
    if request.method == 'POST':
        user_data = request.json
        email = user_data['email']
        password = user_data['password']
        if  not user_data['email'] or not user_data['password']:
            return jsonify({'error': 'Need to fill email or password'}),400
        user = user_collection.find_one({'email': user_data['email']})
        if user and str(user['password']) ==  password:
            access_token = jwt.encode({'email':email}, app.config['SECRET_KEY'], algorithm='HS256')
            print(access_token)
            return jsonify({'access_token': access_token,'message':'Successfully Login'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}),404
    else:
        return render_template('login_page.html')


@app.route('/calculate_estimation', methods=['GET','POST'])
@jwt_required()
def estimate():
    """This route handler (/calculate_estimation) protects with JWT, processes estimation data on POST, calls calculate_estimation function, stores the result with timestamp in database, and returns success/failure message."""
    if request.method == 'POST':
        data = request.get_json()
        print(data)


        estimate,confidence,estimation_range = calculate_estimation(data)

        estimation = {
            "Task": data['Task'],
            "Complexity": data['Complexity'],
            "Size": data['Size'],
            "typeOfTask": data['typeOfTask'],
            "Notes": data['Notes'],
            "Estimate": estimate,
            'Confidence':confidence,
            'Estimation_range':estimation_range,
            'Created_at' : datetime.utcnow()
        }
        result = historical_collection.insert_one(estimation)
        if result:
            return jsonify({'message': 'Estimation submitted successfully!'}), 201
        else:
            return jsonify({"error": "Estimation submitted Not successfully!"}), 404
    return render_template('estimationTool.html')


if __name__ == '__main__':
    app.run(debug=True,port=5020)