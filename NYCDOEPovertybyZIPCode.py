# README
# This code accesses the NYC Open Data API to find data on the number of NYC Department of Education students in a particular ZIP Code who reduce free or reduced lunch or qualify for HRA public benefits

# Information about the NYC DOE's 2013-2018 Demographic Snapshot School Data:
# https://dev.socrata.com/foundry/data.cityofnewyork.us/s52a-8aq6

# API Endpoint
# https://data.cityofnewyork.us/resource/s52a-8aq6.json

# My (John Pham's) app token: QoQet97KEDYpMW4x4Manaflkp

# TO-DO
# * calculate the poverty percentage for an entire ZIP code and output it into a CSV file

import requests
import json

def getPovertyPercentBySchoolDBN(DBN, year="2017-18"):
    getUrl = "https://data.cityofnewyork.us/resource/s52a-8aq6.json"
    parameters = {"dbn":DBN, "year":year, "$$app_token":"QoQet97KEDYpMW4x4Manaflkp"} 
    requestResult = requests.get(getUrl, params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText)
    return jsonText[0]["poverty_2"] #obtain the percentage of students who meet the poverty definition (receive free or reduced lunch or qualify for HRA public benefits)

def getZIPCodebySchoolDBN(DBN):
    getUrl = "https://data.cityofnewyork.us/resource/r2nx-nhxe.json"
    modifiedDBN = DBN + "      " #add white space in order to conform with the data source's formatting
    parameters = {"ats_system_code":modifiedDBN, "$$app_token":"QoQet97KEDYpMW4x4Manaflkp"}
    requestResult = requests.get(getUrl, params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText)
    return jsonText[0]["location_1_zip"] #return the school's ZIP code

def getSchoolsByZIPCode(zipCode):
    getUrl = "https://data.cityofnewyork.us/resource/r2nx-nhxe.json"
    parameters = {"location_1_zip":zipCode, "$$app_token":"QoQet97KEDYpMW4x4Manaflkp"}
    requestResult = requests.get(getUrl, params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText)
    return jsonText

def getPovertyPercentByZIPCode(zipCode, year="2017-18"):
    getUrl = "https://data.cityofnewyork.us/resource/s52a-8aq6.json"
    parameters = {"year":year, "$$app_token":"QoQet97KEDYpMW4x4Manaflkp"} 
    requestResult = requests.get(getUrl, params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText)
    print(len(jsonText))

def printSchoolsPovertyPercentbyZIPCode(zipCode, year="2017-18"):
    schoolsArray = getSchoolsByZIPCode(zipCode)
    for school in schoolsArray:
        schoolDBN = school["ats_system_code"]
        modifiedSchoolDBN = schoolDBN[:-6] #remove last 6 empty white space characters
        povertyPercent = getPovertyPercentBySchoolDBN(modifiedSchoolDBN)
        print(modifiedSchoolDBN + ": " + povertyPercent + "%")

#schoolDBN = "01M015" #01M015 is P.S. 15 Roberto Clemente
#print(schoolDBN + ": " + getPovertyPercentBySchoolDBN("01M015"))
#print(getZIPCodebySchoolDBN(schoolDBN))

zipCode = "11432"
#print(getPovertyPercentByZIPCode(zipCode))
#print(getSchoolsByZIPCode(zipCode))
printSchoolsPovertyPercentbyZIPCode(zipCode)