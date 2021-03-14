
class Disease_Report:
    def __init__(self, id, date, country, cases, disease):
        self._id = id
        self._date = date
        self._country = country
        self._cases = cases
        self._disease = disease
    
    def setID(self, id):
        self._id = id
    
    def getID(self):
        return self._id

    def setDate(self, date):
        self._Date = date
    
    def getDate(self):
        return self._date
    
    def setCountry(self, country):
        self._country = country
    
    def getCountry(self):
        return self._country

    def setCases(self, cases):
        self._cases = cases
    
    def getCases(self):
        return self._cases
    
    def setDisease(self, disease):
        self._disease = disease
    
    def getDisease(self):
        return self._disease
    
    def getJSON(self):
        result = {
            "id": self.getID(),
            "date": self.getDate(),
            "country": self.getCountry(),
            "cases": self.getCases(),
            "disease": self.getDisease(),
        }
        return result