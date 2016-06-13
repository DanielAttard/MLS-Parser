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

        # the result set of a MLS listing
        listing_json = {}
        
        # handling the address information
        listing_json['Address1'] = items[0].span.text.strip()
        listing_json['Address2'] = items[1].span.text.strip()
        listing_json['City'] = items[2].span.text.strip()
        listing_json['Province'] = items[3].span.text.strip()
        listing_json['PostalCode'] = items[4].span.text.strip()
 
        room_counter = 0; # the line number when handling the room information
        rooms = [] # the array of rooms
        room = {} # individual room information
        is_room = False # if current line is about a room

        # start parsing the MLS line by line
        for item in items[5:]:
                

                # handling the (label:value) tuples
                if item.label and item.findAll('span', {'class' : 'value'}) and (not is_room):
                        label = item.label.text[:-1].strip()
                        value = item.span.text.strip()
                        listing_json[label] = value

                # handling the room case
                elif item.text == str(len(rooms)+1):
                        is_room = True

                elif is_room:
                        # every room contains 8 lines

                        if room_counter == 0:
                                room['Number'] = len(rooms)+1
                        elif room_counter == 1:
                                room['Name'] = item.span.text.strip()
                        elif room_counter == 2:
                                room['Level'] = item.span.text.strip()
                        elif room_counter == 3:
                                room['Length'] = item.span.text.strip()
                        elif room_counter == 4:
                                room['Width'] = item.span.text.strip()
                        elif room_counter == 5:
                                room['Feature1'] = item.span.text.strip()
                        elif room_counter == 6:
                                room['Feature2'] = item.span.text.strip()
                        elif room_counter == 7:
                                room['Feature3'] = item.span.text.strip()

                        # reset 
                        if len(room) == 7:
                                rooms.append(room)
                                is_room = False
                                room = {}
                                room_counter = 0
                        else:
                                room_counter = room_counter + 1

        # assign the room information
        listing_json['Rooms'] = rooms

        print listing_json['MLS#']
        print(json.dumps(listing_json, indent = 2))