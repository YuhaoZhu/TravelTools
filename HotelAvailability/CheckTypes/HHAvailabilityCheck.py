from abc import abstractmethod
import urllib, urllib2, cookielib
from CheckTypes.AvailabilityCheck import AvailabilityCheck
from HTMLParsers.HHHTMLParser import HHHTMLParser

PREMIUM_AWARD_CUTOFF = 100000

class HHAvailabilityCheck(AvailabilityCheck):
    @abstractmethod
    def DoCheck(self):
        print("Performing Check: " + str(self))
        data = {
            'searchQuery'           : '',
            'arrivalDate'           : self.startDate.strftime('%d %b %Y'),
            'departureDate'         : self.endDate.strftime('%d %b %Y'),
            'flexibleDates'         : 'true',
            '_flexibleDates'        : 'on',
            'rewardBooking'         : 'true',
            'numberOfRooms'         : 1,
            'numberOfAdults[0]'     : 2,
            'numberOfChildren[0]'   : 0,
            'numberOfAdults[1]'     : 1,
            'numberOfChildren[1]'   : 0,
            'numberOfAdults[2]'     : 1,
            'numberOfChildren[2]'   : 0,
            'numberOfAdults[3]'     : 1,
            'numberOfChildren[3]'   : 0,
            'numberOfAdults[4]'     : 1,
            'numberOfChildren[4]'   : 0,
            'numberOfAdults[5]'     : 1,
            'numberOfChildren[5]'   : 0,
            'numberOfAdults[6]'     : 1,
            'numberOfChildren[6]'   : 0,
            'numberOfAdults[7]'     : 1,
            'numberOfChildren[7]'   : 0,
            'numberOfAdults[8]'     : 1,
            'numberOfChildren[8]'   : 0,
            'promoCode'             : '',
            'groupCode'             : '',
            'corporateId'           : '',
            '_travelAgentRate'      : 'on',
            '_aaaRate'              : 'on',
            '_aarpRate'             : 'on',
            '_seniorRate'           : 'on',
            '_governmentRate'       : 'on',
            'offerId'               : '',
            'bookButton'            : 'false',
            'ctyhocn'               : self.hotelCode,
            'searchType'            : 'PROP',
            'roomKeyEnable'         : 'true'
         }
        data = urllib.urlencode(data)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request('http://www3.hilton.com/en_US/hi/search/findhotels/index.htm', data)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = opener.open(req)
        responseData = response.read()
        
        parser = HHHTMLParser(self.startDate)
        parser.feed(responseData)
        
        #print "Number of points: " + str(parser.numberOfPoints)
        
        if parser.numberOfPoints < PREMIUM_AWARD_CUTOFF and parser.numberOfPoints > 0:
            return [self.startDate]
        else:
            return []