import sys
import requests
from bs4 import BeautifulSoup
import json

link = sys.argv[1]
res = requests.get(link)
soup = BeautifulSoup(res.text, "html.parser")

listings = soup.findAll('div', {'class' : 'hasheader'}, limit=None)

for listing in listings:
        listing_link = listing.get("data-deferred-loaded") if listing.get("data-deferred-loaded") else listing.get("data-deferred-load")
        
        if listing_link is None:
                continue 

        listing_page = requests.get(listing_link)

        items = BeautifulSoup(listing_page.text, "html.parser").findAll('span', {'class' : 'formfield'})

        listing_json = {}
        counter = 0 
        for item in items:
                #print "#", counter, ":", item
                # start parsing the MLS line by line
                if item.findAll('span', {'class' : 'value'}):
                        value = item.span.text.strip()
                        # address information from #0 to #4
                        if counter == 0:
                                listing_json['Address1'] =  value
                        elif counter == 1:
                                listing_json['Address2'] = value
                        elif counter == 2:
                                listing_json['City'] = value
                        elif counter == 3:
                                listing_json['Province'] = value
                        elif counter == 4:
                                listing_json['PostalCode'] = value

                if item.label and item.findAll('span', {'class' : 'value'}):
                        label = item.label.text[:-1].strip()
                        value = item.span.text.strip()
                        listing_json[label] = value
                else:
                        pass
                counter = counter + 1


        print listing_json['MLS#']
        print(json.dumps(listing_json, indent = 4))