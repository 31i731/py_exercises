# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 15:24:30 2019

@author: Vassili Privalihhin
"""

import urllib.request, json
import sys
from datetime import datetime, timedelta
from math import sin, cos, sqrt, atan2, radians

userData = {}

def userlogin(test=False):
    if not test:
        try:
            with urllib.request.urlopen("https://randomuser.me/api/?inc=gender,name,location,nat") as url:
                data = json.loads(url.read().decode()) # loads json from the url
        except:
            sys.exit("Something went wrong while opening url with random user data")
    else:
        try:
            with urllib.request.urlopen("http://127.0.0.1:84/userData.json") as url:
                data = json.loads(url.read().decode()) # loads json from the url
        except:
            sys.exit("Something went wrong while opening url with local fixed user data")

    global userData
    userData = data['results'][0]
    print(userData)
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
    if not test:
        try:
            with urllib.request.urlopen("http://api.open-notify.org/iss-now.json") as url:
                iss = json.loads(url.read().decode())
        except:
            sys.exit("Something went wrong while opening url with iss current coordinates")
    else:
        try:
            with urllib.request.urlopen("http://127.0.0.1:84/iss-now.json") as url:
                iss = json.loads(url.read().decode())
        except:
            sys.exit("Something went wrong while opening url with local fixed iss current coordinates")
    
    print(iss.get("iss_position"))
    if test: print(iss)
    return iss.get("iss_position")

def getIssPassTime(userCoord, test=False):
    if not test:
        urlToOpen = "http://api.open-notify.org/iss-pass.json?lat={}&lon={}&n=1".format(userCoord['latitude'], userCoord['longitude'])
    else:
        urlToOpen = "http://127.0.0.1:84/iss-pass.json"

    try:
        with urllib.request.urlopen(urlToOpen) as url:
            issPassData = json.loads(url.read().decode())
    except urllib.error.HTTPError:
        sys.exit("Couldn't get ISS Pass Time from the server. The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.")

    if test: print("iss pass data: ", issPassData)
    print("iss pass data: ", issPassData)

    try:
        issPassTime = issPassData.get("response")[0].get("risetime")
    except IndexError:
        sys.exit("No response to the request about ISS Pass time")

    return issPassTime

def convertToDateTime(timestamp):
    dateTime = datetime.fromtimestamp(timestamp)
    userOffset = [float(x) for x in getUserTimezone()['offset'].split(":")]
    dateTime = dateTime + timedelta(hours=userOffset[0], minutes=userOffset[1])
    dateTime = dateTime.strftime("%b %d, %Y at %H:%M:%S")
    return dateTime
    
def getPeopleInSpace(test=False):
    if not test:
        try:
            with urllib.request.urlopen("http://api.open-notify.org/astros.json") as url:
                numberOfPeopleInSpace = json.loads(url.read().decode())["number"]
        except:
            sys.exit("Something went wrong while opening url with data of people in space")
    else:
        try:
            with urllib.request.urlopen("http://127.0.0.1:84/astros.json") as url:
                numberOfPeopleInSpace = json.loads(url.read().decode())["number"]
        except:
            sys.exit("Something went wrong while opening url with local fixed data of people in space")

    if test: print("Number of people in space: ", numberOfPeopleInSpace)
    return numberOfPeopleInSpace

def getDistance(userCoord, issCoord):
    # approximate radius of earth in km
    R = 6373.0

    dlon = radians(float(issCoord["longitude"])) - radians(float(userCoord["longitude"]))
    dlat = radians(float(issCoord["latitude"])) - radians(float(userCoord["latitude"]))
    
    a = sin(dlat / 2)**2 + cos(radians(float(userCoord["latitude"]))) * cos(radians(float(issCoord["latitude"]))) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

userlogin()
displayMessage()