from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


app = Flask(__name__)


MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/mydatabase')
client = MongoClient(MONGO_URI)
db = client.get_database() 
employees_collection = db.employees


def serialize_doc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc



@app.route('/employees', methods=['GET'])
def get_all_employees():
    employees = employees_collection.find()
    return jsonify([serialize_doc(doc) for doc in employees])


@app.route('/employees/<string:id>', methods=['GET'])
def get_employee_by_id(id):
    employee = employees_collection.find_one({'_id': ObjectId(id)})
    if employee:
        return jsonify(serialize_doc(employee))
    else:
        return jsonify({"message": "Employee not found"}), 404


@app.route('/employees', methods=['POST'])
def post_employee():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Name is required"}), 400

    result = employees_collection.insert_one({'name': data['name']})
    return jsonify(serialize_doc({'_id': result.inserted_id, 'name': data['name']})), 201



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)