'''
Created on Apr 7, 2015

@author: havlibg
'''

import sqlite3
import urllib2
import smtplib
from HTMLParser import HTMLParser
from smtplib import SMTPException

URL = 'http://www.cruisefish.net/finder.md'
DB = 'cruisecheck.sqlite'

class CruiseHTMLParser(HTMLParser):
    def __init__(self, category):
        HTMLParser.__init__(self)
        self.category = category
        self.bInTable = False
        self.bInSpan = False
        self.bFoundCategory = False
        self.bFoundPrice = False
        self.price = 0
        
    def handle_starttag(self, tag, attrs):
        #Check that we're in the right table
        if self.bInTable:
            #Check that we're at the right category
            if self.bFoundCategory:
                if (tag=='span'): #First span after found category = price
                    self.bFoundPrice = True
            
            #Check for correct category
            else:
                if (tag=='span'):
                    self.bInSpan = True
                    
        #Check for correct table
        else:
            if tag=='table':
                for attr in attrs:
                    if (attr[0]=='id' and attr[1]=='pricetable'):
                        self.bInTable = True
    
    def handle_data(self, data):
        if (self.bFoundPrice):
            self.price = data
            self.bFoundPrice = False
            self.bFoundCategory = False
        
        elif (self.bInSpan):
            if (data==self.category):
                self.bFoundCategory = True
                    
    def handle_endtag(self, tag):
        if (tag=='span'): self.bInSpan = False
        elif (tag=='table'): self.bInTable = False
        
class CruiseCheck(object):
    def __init__(self, checkID, cruiseID, date, category, lastPrice, email):
        self.checkID = checkID
        self.cruiseID = cruiseID
        self.date = date
        self.category = category
        self.lastPrice = lastPrice
        self.email = email
    def __str__(self):
		strSelf = "CheckID: "+str(self.checkID)
		strSelf += " CruiseID: "+str(self.cruiseID)
		strSelf += " Date: "+str(self.date)
		strSelf += " Category: "+str(self.category)
		strSelf += " Last Price: "+str(self.lastPrice)
		strSelf += " Email: "+str(self.email)
		return strSelf
		
    def DoCheck(self):
		print("Performing Check: "+str(self))
		req = urllib2.Request(URL + "?id_cruise=" + str(self.cruiseID))
		response = urllib2.urlopen(req)
		responseData = response.read()
		parser = CruiseHTMLParser(self.category)
		parser.feed(responseData)
		self.newPrice = int(parser.price.replace(",",""))
		if self.newPrice != self.lastPrice:
			print("Price Difference Found.  New Price: " + str(self.newPrice))
			return True
        
def GetChecks():
    vecChecks = []
    
    conn = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    
    curs = conn.cursor()
    for row in curs.execute('SELECT CheckID, CruiseID, Date, Category, LastPrice, Email FROM CruiseChecks'):
        check = CruiseCheck(row["CheckID"], row["CruiseID"], row["Date"], row["Category"], int(row["LastPrice"]), row["Email"])
        vecChecks.append(check)
    
    conn.close()
    
    return vecChecks   
 
def SavePrice(checkID, newPrice):
    conn = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    
    curs = conn.cursor()
    params = (newPrice, checkID)
    curs.execute('UPDATE CruiseChecks SET LastPrice=? WHERE CheckID=?', params)
    conn.commit()
    conn.close()

def DoChecks():
    vecChecks = GetChecks()
    for check in vecChecks:
        if (check.DoCheck()):
            SavePrice(check.checkID, check.newPrice)
            SendEmail(check.email, check.lastPrice, check.newPrice, check.date)
        

def SendEmail(toEmail, oldPrice, newPrice, date):
    emailBody = 'Price has changed for cruise on {0}.  Old price: ${1}, New price: ${2}'.format(date, oldPrice, newPrice)    
    print emailBody
    
    #Get the smtp connection info
    conn = sqlite3.connect('cruisecheck.sqlite')
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute('SELECT host, port, user, pass, fromAddr FROM SMTPInformation')
    smtpinfo = curs.fetchone()
    
    if smtpinfo:
    	#Send email
        try:
            smtpObj = smtplib.SMTP(smtpinfo['host'], int(smtpinfo['port']))
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(smtpinfo['user'], smtpinfo['pass'])
            toAddr = '<{0}>'.format(toEmail)
            message = 'From: {0}\nTo:{1}\nSubject: Cruise Price Change\n\n{2}'.format(smtpinfo['fromAddr'],toAddr,emailBody)
            smtpObj.sendmail(smtpinfo['fromAddr'], toAddr, message)
            smtpObj.quit()
        except SMTPException:
            print 'Error Sending email'
    
if __name__ == '__main__':
    DoChecks()