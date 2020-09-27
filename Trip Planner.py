#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import pandas as pd, numpy as np
import requests
import json
import time


# Parameters
cumul_data = []
counter = 0;
loopCounter = 0;
nextPageExists = True;



print("Welcome to Trip Planner 200 - Need to find hotels or restaurants? We've got you covered")
search_with_space = input("What are you looking for today?: ") 
search = urllib.parse.quote_plus(search_with_space)
print(search)
api_key = input("Please enter your Google API key: ")





while (nextPageExists):
    #print(url)
    
    if (loopCounter == 0):
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+str(search)+'&key='+str(api_key)
        queryResponse = requests.get(url)
        # print(queryResponse.text)
        jsonLoaded = json.loads(queryResponse.text)
        results = jsonLoaded['results']
    else:
        queryResponse = requests.get(url)
        # print(queryResponse.text)
        jsonLoaded = json.loads(queryResponse.text)
        results = jsonLoaded['results']
    for result in results:
        # print(result)
        mondayHours = ""
        tuesdayHours = ""
        wednesdayHours = ""
        thursdayHours = ""
        fridayHours = ""
        saturdayHours = ""
        sundayHours = ""
        address = ""
        phone_number = ""
        name = ""
        website = ""
        category = ""
        hours = ""
        
        place_id = result["place_id"]
        # print(place_id)
        detailedURL = "https://maps.googleapis.com/maps/api/place/details/json?place_id=" + str(place_id) + "&key=" + str(api_key) 
        detailedResponse = requests.get(detailedURL)
        # print(detailedResponse.text)
        detailedJson = json.loads(detailedResponse.text)
        detailedResult = detailedJson['result']
        if 'formatted_address' in detailedResult:
            address = detailedResult['formatted_address']
        if 'formatted_phone_number' in detailedResult:
            phone_number = detailedResult['formatted_phone_number']
        if 'name' in detailedResult:
            name = detailedResult['name']
        if 'website' in detailedResult:
            website = detailedResult['website']
        if 'types' in detailedResult:
            category = detailedResult['types'][0]
        if 'opening_hours' in detailedResult:
            hours = detailedResult["opening_hours"]
            if "weekday_text" in hours:
                weekHours = hours["weekday_text"]
                for dayHour in weekHours:
                    if (counter == 0):
                        mondayHours = dayHour
                        counter +=1
                    elif (counter == 1):
                        tuesdayHours = dayHour
                        counter +=1
                    elif (counter == 2):
                        wednesdayHours = dayHour
                        counter +=1
                    elif (counter == 3):
                        thursdayHours = dayHour
                        counter +=1
                    elif (counter == 4):
                        fridayHours = dayHour
                        counter +=1
                    elif (counter == 5):
                        saturdayHours = dayHour
                        counter +=1
                    elif (counter == 6):
                        sundayHours = dayHour
                        counter +=1
        dataFound = [name, address, phone_number, website, category, mondayHours, tuesdayHours,wednesdayHours,thursdayHours, fridayHours, saturdayHours, sundayHours]
        cumul_data.append(dataFound)
        # print(cumul_data)
        time.sleep(5)
    
    if 'next_page_token' in jsonLoaded:
        print("next page token")
        nextPage = jsonLoaded["next_page_token"]
        loopCounter += 1
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken=" + str(nextPage) + "&key="+str(api_key)
    else:
        nextPageExists = False

print("done")
print(cumul_data)        
columnNames = ["Resource Name", "Address", "Phone Number", "Website", "Category", "Monday Hours", "Tuesday Hours", "Wednesday Hours", "Thursday Hours", "Friday Hours", "Saturday Hours", "Sunday Hours"]
    
export_foodbank_dataframe = pd.DataFrame.from_records(cumul_data, columns=columnNames)
export_foodbank_dataframe.to_csv(r'/Users/Shashank/Documents/Fall-2020-Classes/GB-Work/export_women_shelter_dataframe.csv', index = False, header=True)

