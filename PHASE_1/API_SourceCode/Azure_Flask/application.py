from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import pymongo
import json
import schedule
import os
import time
from geopy.geocoders import Nominatim
from scrape_restrictions import scrape_act_restriction, scrape_nsw_restriction, scrape_nt_restriction, scrape_qld_restriction, scrape_sa_restriction, scrape_tas_restriction, scrape_vic_restriction, scrape_wa_restriction
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.rmrdh.mongodb.net/test?retryWrites=true&w=majority")
database = client["database"]
groups = database["articles"]
log_file = database["log_file"]

@app.route('/')
def hello():
    return render_template("page.html")

def logFile(endpoint, startTime, status):
    endTime = datetime.now()
    timeTook = endTime - startTime
    json_file = open("log_file.txt", "a")
    json_file.write("ENDPOINT: [" + endpoint + "] CURRENT TIME: " + " [" + str(endTime) + "] " + "TIME TAKEN: [" + str(timeTook) + "] STATUS: [" + str(status) + "]\n")

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
def articles():
    time = datetime.now()
    data = request.args
    result = []
    error_msg = checkInvalidDate(data)
    if error_msg:
        error = {
            "timestamp": datetime.now(),
            "status": 400,
            "error":"Bad Request",
            "message": error_msg,
            "path": request.path,
            "client request": request.full_path
        }
        logFile(request.full_path, time, 400)
        return error, 400
    
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
                    #United states for America
                    #check each city, state and country within the geo_locations
                    for geo_location in geo_locations:
                        if article_added:
                            continue
                        if data["location"].lower() in geo_location.lower():
                            correct_location.append(article)
                            article_added = True
        result = correct_location
    
    endTime = datetime.now()
    timeTaken = endTime - time
    #log info with data
    resultMsg = {
        "team_name": "Team Brickwalls",
        "time": str(endTime),
        "time_taken": str(timeTaken),
        "endpoint": request.full_path,
        "status": 200,
        "data": result,
    }
    logFile(request.full_path, time, 200)
    return jsonify(resultMsg)

#gets the current restrictions of each state
#Can pass multiple or no states. Passing no states parameter will get the restrictions of all states.
#e.g. /restrictions?states=nsw,vic
#gets all restrictions of nsw and vic
@app.route('/restrictions', methods=["GET"])
def restrictions():
    time = datetime.now()
    data = request.args
    result = []
    if "states" in data:
        #split the parameter and remove duplicates
        states = data["states"].split(",")
        states = [state.lower() for state in states]
        states = list(dict.fromkeys(states))
        #for each state in the query add the restrictions into the result
        for state in states:
            if state.lower() == "nsw":
                with open("./state_data/nswTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "vic":
                with open("./state_data/vicTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "act":
                with open("./state_data/actTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "nt":
                with open("./state_data/ntTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "qld":
                with open("./state_data/qldTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "sa":
                with open("./state_data/saTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "tas":
                with open("./state_data/tasTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            elif state.lower() == "wa":
                with open("./state_data/waTravelRestriction.json") as json_file:
                    result.append(json.load(json_file))
            else:
                error = {
                    "timestamp": datetime.now(),
                    "status": 400,
                    "error":"Bad Request",
                    "message": "Invalid query, invalid states parameter value. Must be nsw, vic, act, nt, qld, sa, tas or wa. e.g. states=wa,nsw",
                    "path": request.path,
                    "client request": request.full_path
                }
                logFile(request.full_path, time, 400)
                return error, 400
        endTime = datetime.now()
        timeTaken = endTime - time
        #log info with data
        resultMsg = {
            "team_name": "Team Brickwalls",
            "time": str(endTime),
            "time_taken": str(timeTaken),
            "endpoint": request.full_path,
            "status": 200,
            "data": result,
        }
        logFile(request.full_path, time, 200)
        return jsonify(resultMsg)
    else:   
        with open("./state_data/nswTravelRestriction.json") as json_file:
            result.append(json.load(json_file))
        with open("./state_data/vicTravelRestriction.json") as json_file:
            result.append(json.load(json_file))
        with open("./state_data/actTravelRestriction.json") as json_file:
            result.append(json.load(json_file))
        with open("./state_data/ntTravelRestriction.json") as json_file:
            result.append(json.load(json_file))
        with open("./state_data/qldTravelRestriction.json") as json_file:
            result.append(json.load(json_file))
        with open("./state_data/saTravelRestriction.json") as json_file:
            result.append(json.load(json_file))  
        with open("./state_data/tasTravelRestriction.json") as json_file:
            result.append(json.load(json_file)) 
        with open("./state_data/waTravelRestriction.json") as json_file:
            result.append(json.load(json_file))

        endTime = datetime.now()
        timeTaken = endTime - time
        #log info with data
        resultMsg = {
            
            "team_name": "Team Brickwalls",
            "time": str(endTime),
            "time_taken": str(timeTaken),
            "endpoint": request.full_path,
            "status": 200,
            "data": result,
        }
        logFile(request.full_path, time, 200)
        return jsonify(resultMsg)

#TEST
#const fetch = require("node-fetch");
#const response = fetch("http://127.0.0.1:5000/articles?start=20200317&end=20210317")

#TODO REPLACE WITH WEBSCRAPER ADDING ARTICLE EVERY ~24 HOURS
#@app.route('/addReport', methods=["PUT"])
#def addReport():
#    data = request.get_json()
#    if not checkInvalidParam(data):
#        return "Invalid query, only id, date, country, cases and disease are accepted", 400
#    data["_id"] = "PING"
#    groups.insert_one(data)
#    return "Inserted Report to database", 200

def scrape_all():
    #scrape all state restrictions
    scrape_act_restriction()
    scrape_nsw_restriction()
    scrape_nt_restriction()
    scrape_qld_restriction()
    scrape_sa_restriction()
    scrape_tas_restriction()
    scrape_vic_restriction()
    scrape_wa_restriction()
    return

#Create child process to scrape restrictions everyday at 1am
pid=os.fork()
if not pid:
    #child
    #scrape every day at 1am
    schedule.every().day.at("01:00").do(scrape_all)
    while True:
        schedule.run_pending()
        #wait 1 min
        time.sleep(60) 

#scrape_all()

if __name__ == '__main__':
    app.debug = True
    app.run()