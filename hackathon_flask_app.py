from flask import Flask, jsonify
import json
from hacktathon_script import Canpanion
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost"])

canpanion = Canpanion()

@app.route('/login')
@cross_origin(supports_credentials=True)
def login():
    return jsonify({"success" : "ok"})

@app.route('/get_assignments', methods=["GET"])
@cross_origin(origin="localhost", headers=['C   ontent-Type', 'Authorization'])
def assignments():
    due, late = canpanion.get_active_assignments()
    
    result = {
        "LATE_ASSIGNMENTS" : late,
        "DUE_ASSIGNMENTS" : due
        }
    
    print(result)
    
    response = jsonify(result)
    return response

# localhost:5000/get_assignments
# LATE_ASSIGNMENTS
# DUE ASSIGNMENTS

# CLASS_NAME, ASSIGNMENT_NAME, ASSIGNMENT_ID, DUE_DATE, OPEN_UNTIL