from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['Capstone'] # creating database here
user_collection = db['User']

def calculate_estimation(data):
    # Retrieve historical data
    historical_data = list(user_collection.find({
        "complexity": data['complexity'],
        "size": data['size'],
        "type_of_task": data['type_of_task']
    }))
    
    if not historical_data:
        return None, "No historical data available for the given parameters."

    # Extract estimates from historical data
    hist_estimates = []
    for item in historical_data:
        hist_estimates.append(item['estimate'])
    
    # Calculate average estimate
    #avg_estimate = statistics.mean(historical_estimates)
    len_hist = len(hist_estimates)
    count = 0
    for i in hist_estimates:
        count += i
    avg_estimate = count/len_hist
    return avg_estimate,True
