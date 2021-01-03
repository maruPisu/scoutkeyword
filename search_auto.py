import search_auto_single, email_handler
import requests, sys, hashlib, unicodedata
import http.cookiejar as cookielib
from html.parser import HTMLParser

nPages = 6
baseLink = "https://www.autoscout24.es"
cookiesFileName = "cookies.txt"
url = "https://www.autoscout24.es/lst/?sort=age&desc=1&custtype=P&ustate=N%2CU&size=20&page={}&cy=E&priceto=8000&fregfrom=2007&atype=C&"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'From': 'youremail@domain.com', # This is another valid field
}
curSession = requests.Session() 
shaFileName = hashlib.sha1(url.encode('utf-8'))
hashFile = shaFileName.hexdigest()
carFileName = "cars{}.txt".format(hashFile[0:10])
emailBody = ""

class Car:
    name = 'car'
    link = 'not found'
    mileage = 'no mileage'
    year = 'no year'
    city = 'no city'
    description = 'no description'
    image = 'no image'
    
    def __init__(self, initName):
        name = initName
        
    def toString(self):
        print('\n***************\nfound a car: ' + self.name)
        print('link: ' + self.link)
        print('\nmileage: ' + self.mileage)
        print('first registration: ' + self.year)
        print('city: ' + self.city)
        print('description: ' + self.description)
        print('image: ' + self.image)
        
    def appendToEmail(self):
        global emailBody
        carHTML = """\
        <div id = "car">
            <table>
                    <tr>
                    <td>
                        <a href = "{}">
                            <img src = "{}" style="width: 10vw; min-width: 15px;" title = "thumbnail">
                        </a>
                    </td>  
                        <a href = "{}">                  
                                <h2>{}</h2>
                        </a>
                    </tr>
                    <tr>
                <td>
                </td>
                <td>
                <pre>{} - {}</pre>
                </td>
                    </tr>
                    <tr>
                <td>
                </td>
                <td>
                <pre>{}</pre>
                </td>
                    </tr>
                    <tr>
                <td>
                </td>
                <td>
                <pre>{}</pre>
                </td>
                    </tr>
            </table>
            <hr>
        </div>
        """.format(self.link, self.image, self.link, self.name, self.mileage, self.year, self.description, self.city)
        emailBody = emailBody + carHTML
        
    def save(self):
        sha1 = hashlib.sha1(self.link.encode('utf-8'))
        hashLink = sha1.hexdigest()
        cars = []
        try:
            f = open(carFileName)
            cars = f.readlines()
            cars = map(str.strip, cars)
        except IOError:
            print("File not accessible")
        if hashLink not in cars:
            fr = open(carFileName, "a+")
            fr.write(hashLink + "\n")
            self.toString()
            self.appendToEmail()
            
    

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.cars = []
        self.thisCar = Car('noname')
        self.takeNameNext = False
        self.takeMileageNext = False
        self.takeYearNext = False
        self.takeCityNext = False
        
    def handle_starttag(self, tag, attrs):
        #print("Encountered some tag  :", tag)
        takeLink = False
        thisLink = ""
        for name, value in attrs:
            #print('\tattribute {}: {}'.format(name, value))
            if(name == "data-item-name" and value == "detail-page-link"):
                takeLink = True
            if(name == "href"):
                thisLink = baseLink + value
            if(name == "class" and value == "cl-list-element cl-list-element-gap"):
                if(self.thisCar.name != "noname"):
                    self.cars.append(self.thisCar)
                self.thisCar = Car('noname')
                
            if(name == "class" and value == "cldt-summary-makemodel sc-font-bold sc-ellipsis"):
                self.takeNameNext = True
            if(name == "data-type" and value == "mileage"):
                self.takeMileageNext = True
            if(name == "data-type" and value == "first-registration"):
                self.takeYearNext = True
            if(name == "class" and value == "cldt-summary-seller-contact-zip-city"):
                self.takeCityNext = True
            if(tag == "as24-listing-summary-image" and name == "data-images"):
                self.thisCar.image = value.split('/{size}.{format},')[0].encode('utf-8')
        if takeLink:
            takeLink = False
            self.thisCar.link = thisLink
                
    def handle_data(self, data):
        #print("Encountered some data  :", data)
        if(self.takeNameNext):
            self.thisCar.name = data.encode('utf-8').strip()
            unicodedata.normalize('NFKD', self.thisCar.name).encode('ascii', 'ignore')
            self.takeNameNext = False
        if(self.takeMileageNext):
            self.thisCar.mileage = data.encode('utf-8').strip()
            self.takeMileageNext = False
        if(self.takeYearNext):
            self.thisCar.year = data.encode('utf-8').strip()
            self.takeYearNext = False
        if(self.takeCityNext):
            self.thisCar.city = data.encode('utf-8').strip()
            unicodedata.normalize('NFKD', self.thisCar.city).encode('ascii', 'ignore')
            self.takeCityNext = False
            
for currentPage in range(nPages):
    r = curSession.get(url.format(currentPage), headers = headers)

    parser = MyHTMLParser()
    parser.feed(r.text)

    for car in parser.cars:
        if car.name == "car":
            continue
        car.description = search_auto_single.getDescription(car.link)
        unicodedata.normalize('NFKD', car.description).encode('ascii', 'ignore')
        if("carretera" in car.description or "autovia" in car.description or "autopista" in car.description):
            car.save()
if emailBody:
    email_handler.send("pisu.maru@gmail.com", "New cars found", emailBody)
        
    
