from abc import abstractmethod

class AvailabilityCheck(object):
    def __init__(self, startDate, endDate, hotelCode, email):
        self.startDate = startDate
        self.endDate = endDate
        self.hotelCode = hotelCode
        self.email = email
    
    def __str__(self):
        strSelf = "Start Date:" + str(self.startDate)
        strSelf += "End Date:" + str(self.endDate)
        strSelf += "Hotel Code:" + str(self.hotelCode)
        return strSelf
    
    @abstractmethod
    def DoCheck(self): pass