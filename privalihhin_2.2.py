# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 15:24:30 2019

@author: Vassili Privalihhin
"""

import urllib.request, json
from datetime import datetime, timedelta
from math import sin, cos, sqrt, atan2, radians

userData = {}

def userlogin(test=False):
    if not test:
        try:
            with urllib.request.urlopen("https://randomuser.me/api/?inc=gender,name,location,nat") as url:
                data = json.loads(url.read().decode()) # loads json from the url
        except:
            print("Something went wrong while opening url with random user data")
            return
    else:
        try:
            with open('userData.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File 'userData.json' not found")
            return

    global userData
    userData = data['results'][0]
    if test: print("User Data: ", userData)    

def displayMessage():
    getUserName()["title"] += '.'
    fullName = " ".join(getUserName().values())
    distance = int(getDistance(getUserCoordinates(), getIssCoordinates()))
    msg1 = f"Welcome {fullName}. You are now {distance} km away from ISS."

    passTime = convertToDateTime(getIssPassTime(getUserCoordinates()))
    msg2 = f"No worries, ISS will pass by your location in {getUserCity()} on {passTime}."
    msg3 = f"Currently, there are {getPeopleInSpace()} people in space."

    print(msg1)
    print(msg2)
    print(msg3)
    
def getUserName():
    return userData.get("name")

def getUserCoordinates():
    return userData.get("location").get("coordinates")

def getUserCity():
    return userData.get("location").get("city")

def getUserTimezone():
    return userData.get("location").get("timezone")

def getIssCoordinates(test=False):
    try:
        with urllib.request.urlopen("http://api.open-notify.org/iss-now.json") as url:
            iss = json.loads(url.read().decode())
            #print("ISS DATA: ", iss)
    except:
        print("Something went wrong while opening url with iss current coordinates")
        return

    return iss.get("iss_position")

def getIssPassTime(userCoord, test=False):
    urlToOpen = "http://api.open-notify.org/iss-pass.json?lat={}&lon={}&n=1".format(userCoord['latitude'], userCoord['longitude'])
    try:
        with urllib.request.urlopen(urlToOpen) as url:
            issPassData = json.loads(url.read().decode())
    except:
        print("Something went wrong while opening url with iss pass data")
        return

    #print("iss pass data: ", issPassData)
    issPassTime = issPassData.get("response")[0].get("risetime")
    #print("ISS PAST TIME: ", issPassTime)
    return issPassTime


def convertToDateTime(timestamp):
    dateTime = datetime.fromtimestamp(timestamp)
    #print(dateTime)
    userOffset = [float(x) for x in getUserTimezone()['offset'].split(":")]
    dateTime = dateTime + timedelta(hours=userOffset[0], minutes=userOffset[1])
    #print(dateTime)
    dateTime = dateTime.strftime("%b %d, %Y at %H:%M:%S")
    return dateTime
    
def getPeopleInSpace(test=False):
    try:
        with urllib.request.urlopen("http://api.open-notify.org/astros.json") as url:
            numberOfPeopleInSpace = json.loads(url.read().decode())["number"]
    except:
        print("Something went wrong while opening url with data of people in space")
        return

    #print("PEOPLE IN SPACE: ", numberOfPeopleInSpace)
    return numberOfPeopleInSpace

def getDistance(userCoord, issCoord):
    #print(userCoord)
    #print(issCoord)
    
    # approximate radius of earth in km
    R = 6373.0

    dlon = radians(float(issCoord["longitude"])) - radians(float(userCoord["longitude"]))
    dlat = radians(float(issCoord["latitude"])) - radians(float(userCoord["latitude"]))
    
    a = sin(dlat / 2)**2 + cos(radians(float(userCoord["latitude"]))) * cos(radians(float(issCoord["latitude"]))) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance
    
userlogin(test=True)
displayMessage()