import unittest
import requests
import json

#RUN FLASK LOCAL SERVER
#INSTRUCTIONS ARE IN THE GITHUB REPOSITORY README FILE
url = 'http://127.0.0.1:5000/'

class TestRestrictionEndpoint(unittest.TestCase):
    #Test no query, should output all restrictions for all states
    def testNoQuery(self):
        response = requests.get(url + "/restrictions")
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) == 8)
        #list of all Australian states
        states = ["Australian Captital Territory", "New South Wales", "Northern Territory", "Queensland", "South Australia", "Tasmania", "Victoria", "Western Australia"]
        for state_restrictions in data["data"]:
            assert("rules" in state_restrictions)
            #every state must have at least 1 rule
            assert(len(state_restrictions["rules"]) > 1)
            if state_restrictions["state"] in states:
                states.remove(state_restrictions["state"])
        assert(len(states) == 0)

    #Test empty query, should return error
    def testEmptyQuery(self):
        response = requests.get(url + "/restrictions?states=")
        data = json.loads((response.content))
        assert(data["status"] == 400)
        assert(data["error"] == "Bad Request")
        assert(data["message"] == "Invalid query, invalid states parameter value. Must be nsw, vic, act, nt, qld, sa, tas or wa. e.g. states=wa,nsw")
    
    #Test 1 query parameter
    def testSingleQuery(self):
        response = requests.get(url + "/restrictions?states=sa")
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) == 1)
        assert(data["data"][0]["state"] == "South Australia")
        #every state has at least 1 rule
        assert(len(data["data"][0]["rules"]) > 1)
    
    #Test query with multiple states
    def testMultipleQueries(self):
        response = requests.get(url + "/restrictions?states=sa,nsw,vic")
        data = json.loads((response.content))
        assert(data["status"] == 200)
        assert(data["team_name"] == "Team Brickwalls")
        assert("data" in data)
        assert(len(data["data"]) == 3)
        #list of all Australian states in the query
        states = ["New South Wales", "South Australia", "Victoria"]
        for state_restrictions in data["data"]:
            assert("rules" in state_restrictions)
            #every state must have at least 1 rule
            assert(len(state_restrictions["rules"]) > 1)
            if state_restrictions["state"] in states:
                states.remove(state_restrictions["state"])
        assert(len(states) == 0)


if __name__ == '__main__':
    unittest.main()