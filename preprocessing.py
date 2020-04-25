import json
import pymongo
import numpy as np 
import pandas as pd 
from datetime import datetime
from pymongo.errors import BulkWriteError

#pip install pymongo
#pip install dnspython
#pip install pandas

mongo_client = pymongo.MongoClient('localhost',  27017) #default values for mongod
db = mongo_client['gunviolence']['f3'] #change these to whatever collection you want it to be uploaded to

def main():
    gunviolence_df = pd.read_csv('stage3.csv') #change to the shortened stage3 version
    gunviolence_df = gunviolence_df.replace(np.nan, 'undefined', regex=True) #changes all null values to undefined
    
    columns = gunviolence_df.columns
    total_length = len(gunviolence_df)
    doc = {}
    cols = gunviolence_df[columns]
    count = 0
    longitude = 0.0
    latitude = 0.0
    for i in range(total_length):
        doc = {}
        for c in columns:
            if c == 'incident_id':
                #sets the id of the doc to incident_id, casts incident_id to int
                doc['_id'] = int(cols[c][i])
            elif c == 'date':
                #sets the date field, converts to datetime, so that it can be read as ISODate in Mongo
                date = datetime.strptime(cols[c][i], '%Y-%m-%d')
                doc[c] = date
            elif c == 'state' or c == 'city_or_county' or c == 'address' or c == 'latitude' or c == 'longitude' or c == 'location_description':
                if c != 'address' and c != 'location_description':
                #Didn't use address and location description, groups these into location_info field
                    if cols[c][i] != 'undefined':
                        if c == 'latitude' or c == 'longitude':
                        #limits the coordinates to 4 decimal places, it was giving unrounded floats 
                            if c == 'latitude':
                                latitude = round(cols[c][i],4)
                            else:
                                longitude = round(cols[c][i],4)
                            addToDoc('location_info', round(cols[c][i],4), c, doc)
                        else:    
                            addToDoc('location_info', cols[c][i], c, doc)
            elif 'gun' in c:
                if c != 'n_guns_involved':
                    if cols[c][i] != 'undefined':
                        # splits the dictionary and assigns the values to gun_attr
                        splitted = cols[c][i].split('||')
                        for y in range(len(splitted)):
                            gun_id = int(splitted[y][:1])
                            gun_status = splitted[y][3:]
                            if 'gun_info' in doc:
                                if 'gun_attr' in doc['gun_info']:
                                    #checks for missing attributes for certain participants
                                    if gun_id < len(doc['gun_info']['gun_attr']):
                                        doc['gun_info']['gun_attr'][gun_id][c] = gun_status
                                    else: 
                                        doc['gun_info']['gun_attr'].append({'_id': gun_id})
                                        doc['gun_info']['gun_attr'][gun_id][c] = gun_status
                            else:
                                #initializes everything
                                doc['gun_info'] = {}
                                doc['gun_info']['gun_attr'] = []
                                doc['gun_info']['gun_attr'].append({'_id': gun_id})
                                doc['gun_info']['gun_attr'][0][c] = gun_status
                else:
                    if cols[c][i] != 'undefined':
                        addToDoc('gun_info', int(cols[c][i]), c, doc)
            elif 'url' in c or c == 'sources':
                #didn't use these, but too lazy to get rid of 
                pass
                # if 'missing' in c:
                #     addToDoc('sources', bool(cols[c][i]), c, doc)
                # else: 
                #     if '||' in cols[c][i]:
                #         splitted = cols[c][i].split('||')
                #         addToDoc('sources', splitted, c, doc)
                #     else: 
                #         addToDoc('sources', cols[c][i], c, doc)
            elif 'participant' in c:
                if cols[c][i] != 'undefined':
                    splitted = cols[c][i].split('||')
                    for y in range(len(splitted)):
                        if c != 'participant_age':
                            #needs to check for age, to convert the string to int, otherwise mongo will have trouble comparing
                            participant_id = int(splitted[y][:1])
                            participant_info = splitted[y][3:]
                            parts = []
                            if 'participant_info' in doc:
                                for x in doc['participant_info']:
                                    parts.append(x['_id'])
                                if participant_id in parts:
                                    #adds to corresponding index of participant
                                    doc['participant_info'][parts.index(participant_id)][c] = participant_info
                                else:
                                    #if the participant does not exist, add to back
                                    doc['participant_info'].append({'_id' : participant_id})
                                    doc['participant_info'][(len(doc['participant_info']) - 1)][c] = participant_info
                            else:
                                doc['participant_info'] = []
                                doc['participant_info'].append({'_id' : participant_id})
                                doc['participant_info'][0][c] = participant_info
                        else:
                            if '|' not in splitted[y]:
                                participant_id = int(splitted[y][:1])
                                if splitted[y][3:] != '' and ':' not in splitted[y][3:]:
                                    participant_info = int(splitted[y][3:])
                                parts = []
                                if 'participant_info' in doc:
                                    for x in doc['participant_info']:
                                        parts.append(x['_id'])
                                    if participant_id in parts:
                                        doc['participant_info'][parts.index(participant_id)][c] = participant_info
                                    else:
                                        doc['participant_info'].append({'_id' : participant_id})
                                        doc['participant_info'][(len(doc['participant_info']) - 1)][c] = participant_info
                                else:
                                    doc['participant_info'] = []
                                    doc['participant_info'].append({'_id' : participant_id})
                                    doc['participant_info'][0][c] = participant_info
            elif 'house' in c or 'district' in c:
                    if cols[c][i] != 'undefined':
                        addToDoc('law_info', int(cols[c][i]), c, doc)
            elif c == 'n_killed' or c == 'n_injured':
                    addToDoc('casualties', int(cols[c][i]), c, doc)
            else:
                if c == 'incident_characteristics':
                    #parses based on the || characters
                    if '||' in cols[c][i]:
                        splitted = cols[c][i].split('||')
                        addToDoc('misc', splitted, c, doc)
                    else:
                        addToDoc('misc', cols[c][i], c, doc)
        #adding the geospatial coordinates
        geoData = {'type': 'Point', 'coordinates': [longitude, latitude]}
        addToDoc('location_info', geoData, 'geo', doc)
        #writes to database, one by one, multiple write was giving issues
        rec_id1 = db.insert_one(doc)
        count+=1
        if count % 50000 == 0:
            print(count)        
    
    print("DONE!")

    #creates the Geospatial Index
    db.create_index([('location_info.geo', pymongo.GEOSPHERE)])
    print("Geo Index Created!")
    #print(doc)





def addToDoc(key, value, c, doc):
    if key in doc: 
        doc[key][c] = value
    else:
        doc[key] = {}
        doc[key][c] = value
        
if __name__ == '__main__':
    main()




