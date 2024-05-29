from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['Capstone'] # creating database here
user_collection = db['User']

def calculate_estimation(data):
    # Retrieve historical data
    historical_data = list(user_collection.find({
        "Complexity": data['Complexity'],
        "Size": data['Size'],
        "typeOfTask": data['typeOfTask']
    }))
    
    if not historical_data:
        return 0, 'low','0.0-0.0'

    # Extract estimates from historical data
    hist_estimates = []
    for item in historical_data:
        hist_estimates.append(item['estimate'])
    if not hist_estimates:
        return jsonify({"efforted_time":1,"confiden":"low","effort_range":'0-0'})
    
    # Calculate average estimate
    #avg_estimate = statistics.mean(historical_estimates)
    len_hist = len(hist_estimates)
    count = 0
    for i in hist_estimates:
        count += i
    avg_estimate = count/len_hist
    to_cal = sum([(est-avg_estimate)**2 for est in hist_estimates])
    var = to_cal/len(hist_estimates)
    deviation = var**0.5
    lowerBoundary = avg_estimate-deviation
    higherBoundary = avg_estimate+deviation
    if deviation<5:
        confidence = 'low'
    elif deviation<10:
        confidence = 'medium'
    else:
        confidence = 'high'
    estimation_range = f'{lowerBoundary} - {higherBoundary}'
    return avg_estimate,confidence,estimation_range
