from flask import Flask, request, jsonify, render_template
from datetime import datetime
import pymongo
from geopy.geocoders import Nominatim

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.rmrdh.mongodb.net/test?retryWrites=true&w=majority")
database = client["database"]
groups = database["articles"]

@app.route('/')
def hello():
    return render_template("page.html")

#used to check if the start and end dates are valid
#will check if they exist and if start date is before end date 
def checkInvalidDate(requestData):
    found_start = False
    found_end = False
    #checks if both start and end paramters exist
    for elem in requestData:
        if elem == "start":
            found_start = True
        if elem == "end":
            found_end = True
    if not found_start or not found_end:
        return "Invalid query, please provide both start and end dates"
    try:
        start = datetime.strptime(requestData["start"], "%Y%m%d").date()
        end = datetime.strptime(requestData["end"], "%Y%m%d").date()
    except ValueError:
        return "Invalid query, date is invalid. Format must be YYYYmmdd"
    #checks if start date is before end date
    if start > end:
        return "Invalid query, end date must be after start date"
    else:
        return ""

#parse queries to search for articles
#e.g /articles?start=20190701&end=20200901&location=Sydney&keyterms=illness
#will return all articles between 1/7/2019 and 1/9/2020, have disease reports within Sydney and have the keyterm "illness"

@app.route('/articles', methods=["GET"])
def getReport():
    data = request.args
    result = []
    error_msg = checkInvalidDate(data)
    if error_msg:
        error = {
            "timestamp": datetime.strptime(str(datetime.now().strftime("%Y%m%d")), "%Y%m%d"),
            "status": 400,
            "error":"Bad Request",
            "message": error_msg,
            "path": request.path,
            "client request": request.full_path
        }
        return error
    
    #Get all articles within the specified date
    correct_date = []
    start_search = datetime.strptime(data["start"], "%Y%m%d").date()
    end_search = datetime.strptime(data["end"], "%Y%m%d").date()
    #groups.find({}) gets all articles from database
    for article in groups.find({}):
        start_input = datetime.strptime(article["date_of_publication"], "%Y-%m-%d").date()
        end_input = datetime.strptime(article["date_of_publication"], "%Y-%m-%d").date()
        if start_search < start_input and end_search > end_input:
            #_id prevents object from being jsonified
            del article["_id"]
            correct_date.append(article)
    result = correct_date

    #From the collected articles with the correct dates, get all articles with correct key terms. This is optional as keyterms is not required
    #An article/report has a keyterm if the keyterm can be found in he article headline, article main text, report disease, location or syndrome
    correct_keyterms = []
    if 'keyterms' in data:
        terms = data["keyterms"].split(",")
        #result contains all articles with dates within the start and end dates passed in the query
        for article in result:
            #article_added prevents the same article being added twice in case it contains more than 1 key term
            article_added = False
            #check all attributes if the key term can be found
            for term in terms:
                if article_added:
                    continue
                if term.lower() in article["headline"].lower():
                    correct_keyterms.append(article)
                    article_added = True
                elif term.lower() in article["main_text"].lower():
                    correct_keyterms.append(article)
                    article_added = True
                else:
                    for report in article["reports"]:
                        for disease in report["diseases"]:
                            if term.lower() in disease.lower():
                                correct_keyterms.append(article)
                                article_added = True
                                break
                        for location in report["locations"]:
                            if term.lower() in location.lower():
                                correct_keyterms.append(article)
                                article_added = True
                                break
                        for syndrome in report["syndromes"]:
                            if term.lower() in syndrome.lower():
                                correct_keyterms.append(article)
                                article_added = True
                                break
        result = correct_keyterms

    #From the collected articles with the correct dates or correct key terms, get all articles with disease reports with the correct location.
    #This is the same case as the keyterms, as it is optional and can be skipped. It can also be searched for straight after checking for correct date if no keyterm was passed.
    #Will check all reports in the article and check if the report location is the same as the location query.
    #Added functionality so that now searching for a country will also get reports with locations of cities and states within the country
    geolocator = Nominatim(user_agent = "geoapiExercises")

    correct_location = []
    if "location" in data:
        #for each article in the remaining list of articles
        for article in result:
            article_added = False
            #check each report for each article
            for report in article["reports"]:
                if article_added:
                    continue
                #check each location within each report
                for location in report["locations"]:
                    if article_added:
                        continue
                    #gets city, state and country info from the report location
                    #e.g. passing Sydney will return Sydney, New South Wales, Australia
                    loc = geolocator.geocode(location, language='en')
                    geo_locations = str(loc).split(', ')
                    #check each city, state and country within the geo_locations
                    for geo_location in geo_locations:
                        if article_added:
                            continue
                        if data["location"].lower() in geo_location.lower():
                            correct_location.append(article)
                            article_added = True
        result = correct_location
    return jsonify(result)

#TEST
#const fetch = require("node-fetch");
#const response = fetch("http://127.0.0.1:5000/reports?start=20200317&end=20210317")

#DELETE ADD REPORT ENDPOINT
#TODO REPLACE WITH WEBSCRAPER ADDING ARTICLE EVERY ~24 HOURS
#@app.route('/addReport', methods=["PUT"])
#def addReport():
#    data = request.get_json()
#    if not checkInvalidParam(data):
#        return "Invalid query, only id, date, country, cases and disease are accepted", 400
#    data["_id"] = "PING"
#    groups.insert_one(data)
#    return "Inserted Report to database", 200


if __name__ == '__main__':
    app.debug = True
    app.run()