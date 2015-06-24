from abc import abstractmethod
import urllib, urllib2, json
from datetime import date, timedelta
from CheckTypes.AvailabilityCheck import AvailabilityCheck

class IHGAvailabilityCheck(AvailabilityCheck):
    @abstractmethod
    def DoCheck(self):
        print("Performing Check: " + str(self))
        vecFoundDates = []
        
        data = {
                    'hotelCode'     : self.hotelCode,
                    'rateCode'      : 'IVANI',
                    'startMonth'    : self.startDate.month-1,
                    'startYear'     : self.startDate.year
                }
        data = urllib.urlencode(data)
        req = urllib2.Request('https://www.ihg.com/hotels/us/en/reservation/bulkavail', data)
        response = urllib2.urlopen(req)
        responseData = response.read()
        jsonData = json.loads(responseData)
        if 'availabledate' in jsonData:
            #print("Available Dates:" + str(jsonData['availabledate']))
            
            #make our list of dates to availabilitycheck
            tempDate = self.startDate
            vecDesiredDates = []
            while tempDate != self.endDate:
                vecDesiredDates.append(tempDate)
                tempDate = tempDate + timedelta(days=1)
                
                
            #go through available dates
            for strAvailableDate in jsonData['availabledate']:
                splitAvailableDate = strAvailableDate.split('-')
                availableDate = date(int(splitAvailableDate[0]), int(splitAvailableDate[1]), int(splitAvailableDate[2]))
                for desiredDate in vecDesiredDates:
                    if desiredDate == availableDate:
                        vecFoundDates.append(availableDate)
        else:
            print ("No available dates")
        
        return vecFoundDates