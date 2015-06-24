from HTMLParser import HTMLParser

class HHHTMLParser(HTMLParser):
    def __init__(self, desiredDate):
        HTMLParser.__init__(self)
        self.desiredDate = desiredDate.strftime('%m/%d/%Y')
        self.numberOfPoints = -1
        self.bInTable = False
        self.bFoundCorrectRow = False
        self.bFoundPoints = False
    
    def handle_starttag(self, tag, attrs):
        #Check that we're in the correct table
        if self.bInTable:
            #Check that  we're in the correct row
            if self.bFoundCorrectRow:
                #Strong with class 'priceSpanPricePerNight' contains points
                if (tag=='strong'):
                    for attr in attrs:
                        if (attr[0]=='class' and attr[1]=='priceSpanPricePerNight'):
                            self.bFoundPoints = True
            else:
                #Input with value containing our date means we're in the right row
                if (tag=='input'):
                    for attr in attrs:
                        if (attr[0]=='value' and self.desiredDate in attr[1]):
                            self.bFoundCorrectRow = True
        
        #Check for correct table
        else:
            if (tag=='table'):
                for attr in attrs:
                    if (attr[0]=='class' and attr[1]=='tblAvailCal'):
                        self.bInTable = True
    
    def handle_data(self, data):
        if self.bFoundPoints:
            self.numberOfPoints = int(data.replace(',',''))
    
    def handle_endtag(self, tag):
        if (tag=='table'): self.bInTable = False
        elif (tag=='tr'): self.bFoundCorrectRow = False
        elif (tag=='strong'): self.bFoundPoints = False