import unittest
import requests
import json
from geopy.geocoders import Nominatim

#RUN FLASK LOCAL SERVER
#INSTRUCTIONS ARE IN THE GITHUB REPOSITORY README FILE
url = 'http://127.0.0.1:5000/'

class TestArticleEndpoint(unittest.TestCase):
    #Test if no dates are passed
    #Should return error
    def testNoDates(self):
        response = requests.get(url + "/articles")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, please provide both start and end dates")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?")

    #Test if one of the dates are passed
    #Should return error
    def testOneDate(self):
        #only start date
        response = requests.get(url + "/articles?start=20105490")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, please provide both start and end dates")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?start=20105490")
        #only end date
        response = requests.get(url + "/articles?end=20105490")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, please provide both start and end dates")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?end=20105490")

    #Test if invalid formatted dates are passed
    #Should return error
    def testInvalidFormDates(self):
        #Test if both are formatted wrong
        response = requests.get(url + "/articles?start=201054901&end=200013142")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, date is invalid. Format must be YYYYmmdd")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?start=201054901&end=200013142")

        #Test if start is formatted wrong
        response = requests.get(url + "/articles?start=201054901&end=20001102")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, date is invalid. Format must be YYYYmmdd")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?start=201054901&end=20001102")

        #Test if end is formatted wrong
        response = requests.get(url + "/articles?start=20100401&end=20001302")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, date is invalid. Format must be YYYYmmdd")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?start=20100401&end=20001302")
    
    #Test if start date is after end date
    #Should return error
    def testInvalidDateRange(self):
        #start is after end date
        response = requests.get(url + "/articles?start=20100401&end=20001202")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, end date must be after start date")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?start=20100401&end=20001202")
    
    #Test if start date and end dates are the same
    def testSameDate(self):
        response = requests.get(url + "/articles?start=20000401&end=20211202")
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        #check if article and report has all correct attributes
        for article in data["data"]:
            assert("date_of_publication" in article)
            assert("headline" in article)
            assert("main_text" in article)
            assert("reports" in article)
            for report in article["reports"]:
                assert("diseases" in report)
                assert("event_date" in report)
                assert("locations" in report)
                assert("syndromes" in report)

    #Test valid dates and check output
    def testValidDate(self):
        response = requests.get(url + "/articles?start=20000401&end=20211202")
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) > 1)
        #check if article and report has all correct attributes
        for article in data["data"]:
            assert("date_of_publication" in article)
            assert("headline" in article)
            assert("main_text" in article)
            assert("reports" in article)
            for report in article["reports"]:
                assert("diseases" in report)
                assert("event_date" in report)
                assert("locations" in report)
                assert("syndromes" in report)
    
    #Test keyterm query and check if keyterm is in the output
    #Test multiple keyterms
    def testKeyTerms(self):
        keyterm = "case"
        response = requests.get(url + "/articles?start=20000401&end=20211202&keyterms=" + keyterm)
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) > 1)
        #check if article and report has all correct attributes
        #check if keyterm is in all of the articles
        for article in data["data"]:
            found_keyterm = False
            assert("date_of_publication" in article)
            #key term could be in headline
            assert("headline" in article)
            if keyterm.lower() in article["headline"].lower():
                found_keyterm = True
            #key term could be in main text
            assert("main_text" in article)
            if keyterm.lower() in article["headline"].lower():
                found_keyterm = True

            assert("reports" in article)

            for report in article["reports"]:
                #key term could be in list of diseases
                assert("diseases" in report)
                for disease in report["diseases"]:
                    if keyterm.lower() in disease.lower():
                        found_keyterm = True

                assert("event_date" in report)
                #key term could be in list of locations
                assert("locations" in report)
                for location in report["locations"]:
                    if keyterm.lower() in location.lower():
                        found_keyterm = True
                #key term could be in list of syndromes
                assert("syndromes" in report)
                for syndrome in report["syndromes"]:
                    if keyterm.lower() in syndrome.lower():
                        found_keyterm = True
            #will be true if keyterm found in article
            assert(found_keyterm)
        
        #test multiple key terms
        keyterm = "case,illness"
        keyterms = ["case", "illness"]
        response = requests.get(url + "/articles?start=20000401&end=20211202&keyterms=" + keyterm)
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) > 1)
        #check if article and report has all correct attributes
        #check if keyterm is in all of the articles
        for article in data["data"]:
            found_keyterm = False
            assert("date_of_publication" in article)
            #key term could be in headline
            assert("headline" in article)
            for term in keyterms:
                if term.lower() in article["headline"].lower():
                    found_keyterm = True
            #key term could be in main text
            assert("main_text" in article)
            for term in keyterms:
                if term.lower() in article["headline"].lower():
                    found_keyterm = True

            assert("reports" in article)

            for report in article["reports"]:
                #key term could be in list of diseases
                assert("diseases" in report)
                for disease in report["diseases"]:
                    for term in keyterms:
                        if term.lower() in disease.lower():
                            found_keyterm = True

                assert("event_date" in report)
                #key term could be in list of locations
                assert("locations" in report)
                for location in report["locations"]:
                    for term in keyterms:
                        if term.lower() in location.lower():
                            found_keyterm = True
                #key term could be in list of syndromes
                assert("syndromes" in report)
                for syndrome in report["syndromes"]:
                    for term in keyterms:
                        if keyterm.lower() in syndrome.lower():
                            found_keyterm = True
            #will be true if keyterm found in article
            assert(found_keyterm)
    
    #Test location query and check if location is in output
    def testLocation(self):
        location = "United States"
        response = requests.get(url + "/articles?start=20000401&end=20211202&location=" + location)
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) > 1)
        geolocator = Nominatim(user_agent = "geoapiExercises")
        #check if article and report has all correct attributes
        #check if article location refers to location in query
        for article in data["data"]:
            found_location = False
            assert("date_of_publication" in article)
            assert("headline" in article)
            assert("main_text" in article)
            assert("reports" in article)
            for report in article["reports"]:
                assert("diseases" in report)
                assert("event_date" in report)
                assert("locations" in report)
                #check all locations if the query location exists
                for location in report["locations"]:
                    #used to check for specific detail of location
                    #e.g. query search wants Australia therefore states of Australia and cities would count
                    loc = geolocator.geocode(location, language='en')
                    geo_locations = str(loc).split(', ')
                    for geo_location in geo_locations:
                        if location.lower() in geo_location.lower():
                            found_location = True
                assert("syndromes" in report)
            #checks if location was within the article
            assert(found_location)

    #Test all queries (location and keyterms) and ensure all are in the output
    def testAll(self):
        location = "United States"
        keyterm = "case"
        response = requests.get(url + "/articles?start=20000401&end=20211202&location=" + location + "&keyterms=" + keyterm)
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) > 1)
        geolocator = Nominatim(user_agent = "geoapiExercises")
        #check if article and report has all correct attributes
        #check if article location refers to location in query
        for article in data["data"]:
            found_keyterm = False
            found_location = False
            assert("date_of_publication" in article)
            #key term could be in headline
            assert("headline" in article)
            if keyterm.lower() in article["headline"].lower():
                found_keyterm = True
            #key term could be in main text
            assert("main_text" in article)
            if keyterm.lower() in article["headline"].lower():
                found_keyterm = True

            assert("reports" in article)

            for report in article["reports"]:
                #key term could be in list of diseases
                assert("diseases" in report)
                for disease in report["diseases"]:
                    if keyterm.lower() in disease.lower():
                        found_keyterm = True

                assert("event_date" in report)
                #key term could be in list of locations
                assert("locations" in report)
                for location in report["locations"]:
                    loc = geolocator.geocode(location, language='en')
                    geo_locations = str(loc).split(', ')
                    for geo_location in geo_locations:
                        if location.lower() in geo_location.lower():
                            found_location = True
                    if keyterm.lower() in location.lower():
                        found_keyterm = True
                #key term could be in list of syndromes
                assert("syndromes" in report)
                for syndrome in report["syndromes"]:
                    if keyterm.lower() in syndrome.lower():
                        found_keyterm = True
            #will be true if keyterm found in article
            assert(found_keyterm)
            assert(found_location)


if __name__ == '__main__':
    unittest.main()