from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pymongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.rmrdh.mongodb.net/test?retryWrites=true&w=majority")
database = client["Report_database"]
groups = database["Reports"]

@app.route('/')
def hello():
    return render_template("page.html")

def checkInvalidParam(requestData):
    for elem in requestData:
        if elem != "id" and elem != "date" and elem != "country" and elem != "cases" and elem != "disease":
            return False
    return True

#parse queries to search for disease reports
#e.g /getReport?country=Australia
#will return all reports of the country Australia

@app.route('/getReport', methods=["GET"])
def getReport():
    result = []
    filters = {}
    if request.args:
        filters = request.args
        if not checkInvalidParam(filters):
            return "Invalid query, only id, date, country, cases and disease are accepted", 400
    for report in groups.find(filters):
        result.append(report)
    if len(result) == 0:
        return "No disease reports found", 404
    return jsonify(result)

#parse JSON disease report to add to database
#e.g javascript example
#const response = fetch("http://127.0.0.1:5000/addReport", {
#    method: "PUT",
#    headers: {
#        'Accept': 'application/json',
#        'Content-Type': 'application/json'
#    },
#    body: JSON.stringify({ 
#        "date": "2020-5-6",
#        "country": "India",
#        "cases": 2,
#        "disease": "ebola",
#    })
#})
@app.route('/addReport', methods=["PUT"])
def addReport():
    data = request.get_json()
    if not checkInvalidParam(data):
        return "Invalid query, only id, date, country, cases and disease are accepted", 400
    data["_id"] = "PING"
    groups.insert_one(data)
    return "Inserted Report to database", 200

if __name__ == '__main__':
    app.debug = True
    app.run()