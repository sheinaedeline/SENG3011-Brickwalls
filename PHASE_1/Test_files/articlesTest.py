import unittest
import requests
import json

#RUN FLASK LOCAL SERVER
#INSTRUCTIONS ARE IN THE GITHUB REPOSITORY README FILE
url = 'http://127.0.0.1:5000/'

class TestArticleEndpoint(unittest.TestCase):
    #Test if no dates are passed
    def testNoDates(self):
        response = requests.get(url + "/articles")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, please provide both start and end dates")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?")

    #Test if one of the dates are passed
    def testOneDate(self):
        #only start date
        response = requests.get(url + "/articles?start=20105490")
        data = json.loads((response.content))
        print(data)
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
    
    def testInvalidDateRange(self):
        #start is after end date
        response = requests.get(url + "/articles?start=20100401&end=20001202")
        data = json.loads((response.content))
        assert(data["message"] == "Invalid query, end date must be after start date")
        assert(data["status"] == 400)
        assert(data["path"] == "/articles")
        assert(data["client request"] == "/articles?start=20100401&end=20001202")
    
    def testValidDate(self):
        response = requests.get(url + "/articles?start=20000401&end=20201202")
        data = json.loads((response.content))
        print(data)





if __name__ == '__main__':
    unittest.main()