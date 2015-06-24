'''
Created on Jan 8, 2015

@author: havlibg
'''

import sqlite3
import smtplib
from smtplib import SMTPException
from CheckTypes.HHAvailabilityCheck import HHAvailabilityCheck
from CheckTypes.IHGAvailbilityCheck import IHGAvailabilityCheck

TYPE_IHG = 'ihg'
TYPE_HH = 'hh'

def DoChecks():
    vecChecks = GetChecks()
    for check in vecChecks:
        vecFoundDates = check.DoCheck()
        if len(vecFoundDates) > 0:
            SendEmail(check.email, check.hotelCode, vecFoundDates)
            pass
    
def GetChecks():
    vecChecks = []
    
    conn = sqlite3.connect('hotelcheck.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    
    curs = conn.cursor()
    for row in curs.execute('SELECT startDate, endDate, hotelCode, email, type FROM AvailabilityChecks'):
        if (row['type']==TYPE_IHG):
            check = IHGAvailabilityCheck(row["startDate"], row["endDate"], row["hotelCode"], row["email"])
        elif (row['type']==TYPE_HH):
            check = HHAvailabilityCheck(row["startDate"], row["endDate"], row["hotelCode"], row["email"])
        else:
            continue
        
        vecChecks.append(check)
    
    return vecChecks
        
def SendEmail(email, hotelCode, vecDates):    
    conn = sqlite3.connect('hotelcheck.sqlite')
    conn.row_factory = sqlite3.Row
    
    curs = conn.cursor()
    
    #Get the smtp connection info
    curs.execute('SELECT host, port, user, pass, fromAddr FROM SMTPInformation')
    smtpinfo = curs.fetchone()
    
    #Get the hotel name and build email body
    params = (hotelCode, )
    curs.execute('SELECT name, city, state, country FROM HotelCodes WHERE code=?', params)
    row = curs.fetchone()
    if row:
        emailBody = 'Availability has been found at {0}, {1}, {2}, {3} on the following dates: '.format(row['name'], row['city'], row['state'], row['country'])
    else:
        emailBody = 'Availability has been found at {0} on the following dates: '.format(hotelCode)
    
    for date in vecDates:
        emailBody = emailBody + date.strftime('%m/%d/%Y') + ', '
    
    emailBody = emailBody[:-2]
    
    print emailBody+"\n"
    
    if smtpinfo:
        #Send email
        try:
            smtpObj = smtplib.SMTP(smtpinfo['host'], int(smtpinfo['port']))
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(smtpinfo['user'], smtpinfo['pass'])
            toAddr = '<{0}>'.format(email)
            message = 'From: {0}\nTo:{1}\nSubject: Availability Found\n\n{2}'.format(smtpinfo['fromAddr'],toAddr,emailBody)
            smtpObj.sendmail(smtpinfo['fromAddr'], toAddr, message)
            smtpObj.quit()
        except SMTPException:
            print 'Error Sending email'
        
