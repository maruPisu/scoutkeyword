import requests
import http.cookiejar as cookielib
from html.parser import HTMLParser

curSession = requests.Session() 

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.description = "no description"
        self.takeDescriptionNext = False
        
    def handle_starttag(self, tag, attrs):
        #print("Encountered some tag  :", tag)        
        for name, value in attrs:
            if(name == "data-type" and value == "description"):
#                print('\tattribute {}: {}'.format(name, value))
                self.takeDescriptionNext = True
                
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if(self.takeDescriptionNext):
            self.description = data.strip()
            self.takeDescriptionNext = False
            
def getDescription(url):            
    r = curSession.get(url)

    parser = MyHTMLParser()
    parser.feed(r.text)
    
    return parser.description