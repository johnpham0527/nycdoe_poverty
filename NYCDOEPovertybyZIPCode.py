# README
# This code accesses the NYC Open Data API to find data on the number of NYC Department of Education students in a particular ZIP Code who reduce free or reduced lunch or qualify for HRA public benefits

# Information about the NYC DOE's 2013-2018 Demographic Snapshot School Data:
# https://dev.socrata.com/foundry/data.cityofnewyork.us/s52a-8aq6

# API Endpoint
# https://data.cityofnewyork.us/resource/s52a-8aq6.json

# My (John Pham's) app token: QoQet97KEDYpMW4x4Manaflkp

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

def getNumSchoolsByZIPCode(zipCode):
    return len(getSchoolsByZIPCode(zipCode))

def getPovertyPercentByZIPCode(zipCode, year="2017-18"):
    print("Retrieving school poverty data...")
    schoolsArray = getSchoolsByZIPCode(zipCode) #generate a list of schools in the given ZIP code
    enrollmentArray = []
    povertyCountArray = []

    for school in schoolsArray: #loop through the list of schools 
        schoolDBN = school["ats_system_code"] #obtain each school's DBN
        modifiedSchoolDBN = schoolDBN[:-6] #remove last 6 empty white space characters

        getUrl = "https://data.cityofnewyork.us/resource/s52a-8aq6.json"
        parameters = {"dbn":modifiedSchoolDBN, "year":year, "$$app_token":"QoQet97KEDYpMW4x4Manaflkp"} 
        requestResult = requests.get(getUrl, params=parameters) #submit the GET request
        resultText = requestResult.text #obtain the requested text
        jsonText = json.loads(resultText)

        povertyPercent = jsonText[0]["poverty_2"]

        enrollment = jsonText[0]["total_enrollment"] #obtain the school's total enrollment
        enrollmentArray.append(enrollment)
        povertyCount = jsonText[0]["poverty_1"] #obtain the number of students in the school 
        povertyCountArray.append(povertyCount)
        
        print("School DBN: " + modifiedSchoolDBN + "\tPoverty Percentage: " + povertyPercent + "%" + "\tPoverty Count: " + povertyCount + "\tTotal Enrollment: " + enrollment)

    enrollmentSum = 0
    for i in enrollmentArray:
        enrollmentSum += float(i)

    povertySum = 0
    for j in povertyCountArray:
        povertySum += float(j)

    print("Total Number of Students with Poverty Status: " + str(povertySum))
    print("Total Number of Students Enrolled in ZIP Code: " + str(enrollmentSum))

    ZIPCodePovertyPercentage = povertySum / enrollmentSum * 100 #calculate the percentage of students who receive free or reduced lunch or qualify for HRA public benefits
    return ZIPCodePovertyPercentage



#schoolDBN = "01M015" #01M015 is P.S. 15 Roberto Clemente
#print(schoolDBN + ": " + getPovertyPercentBySchoolDBN("01M015"))
#print(getZIPCodebySchoolDBN(schoolDBN))

zipCode = "11432"

#print(getSchoolsByZIPCode(zipCode))
#printSchoolsPovertyPercentbyZIPCode(zipCode)

#Print the ZIP code's average NYC DOE poverty percentage.
print("There are " + str(getNumSchoolsByZIPCode(zipCode)) + " schools in ZIP Code " + str(zipCode) + ". ")
print("This ZIP Code's average NYC DOE poverty percentage is " + str(round(getPovertyPercentByZIPCode(zipCode),1)) + "%.")