from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
client = MongoClient("mongodb://locolhost:27017/")
db = client['Capston'] # creating database here
user_collection = db['User'] # defining / creating User collection
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.json()
        name = data['name']
        email = data['email']
        contact = data['contact']
        password = data['password']
        if not name and not email and not contact and not password:
            return jsonify({'error':"All fields input required"}), 400
        if user_collection.find_one({'email': email}):
            return jsonify({"error": "User already exists"}), 401
        user_collection.insert_one({'name': name, 'email':email, 'contact': contact, 'password': password})
        return jsonify({"message": "User registered successfully"}), 201
    return render_template('registration.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        data = request.json()
        email = data['email']
        password = data['password']
        if not email and not password:
            return jsonify({'error':'Need to fill email or password'})
        user = user_collection.find_one({'email': email}), 400
        if user and user['password'] ==  password:
            access_token = create_access_token(identity={'email': email})
            return jsonify({'access_token': access_token,'message':"Login Successfully completed"}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    return render_template('login_page.html')

@app.route('/submit_estimation', methods=['POST'])
@jwt_required()
def submit_estimation():
    data = request.get_json()
    current_user = get_jwt_identity()
    
    estimation = {
        'username': current_user['username'],
        'task': data['task'],
        'complexity': data['complexity'],
        'size': data['size'],
        'type': data['type'],
        'notes': data['notes'],
        'timestamp': datetime.utcnow()
    }
    
    mongo.db.estimations.insert_one(estimation)
    return jsonify({"message": "Estimation submitted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)