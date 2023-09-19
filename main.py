import requests
import os
from bs4 import BeautifulSoup

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


def powayUnifiedEvents(school,startYear,endYear):
    outputText = ''
    outputText +=('Running '+str(school)+' for years: '+str(startYear)+' '+str(endYear))

    targetStrings = ['Bell Schedule', 'Schedule', 'No School']
    for year in range (startYear,endYear+1):
        for i in range(0, 11):
            modifiedDays = 0
            dayString = ''
            # Get the request for each month
            url = 'https://'+school+'.powayusd.com/apps/events/' + str(year) + '/' + str(i + 1) + '/?id=0&id=1'
            r = requests.get(url)
            if r.status_code == 200:
                # Request Successful

                # create a soup object
                s = BeautifulSoup(r.text, 'html.parser')
                # find all event elements
                eventElements = s.find_all('a', class_='event-link')

                # loop through event elements and extract calander dates
                for e in eventElements:
                    for t in targetStrings:
                        if t in e.getText():
                            modifiedDays += 1
                            dayString += e.get('aria-label') + '\n'
                            continue

                #print out the findings for that month
                if modifiedDays != 0:
                    outputText += (months[i]+' '+str(year)+':\nModified Days: '+str(modifiedDays)+'\n'+dayString)
    print('Completed '+school+' Processing\n')

    #Output findings to a file
    outputFileName = str(school) + str(startYear) + str(endYear)+'output.txt'
    with open(outputFileName, 'w') as file:
        file.write(outputText)

if __name__ == '__main__':
    startYear = 2023
    endYear = 2024
    targetMonth = 110
    cwd = os.getcwd()
    schools = ['delnorte','montereyridge','stoneranch','delsur','design39campus']

    #Searching Poway Unified School events
    for school in schools:
        powayUnifiedEvents(school,startYear,endYear)

    #Got a specific month of info we're searching for? set the targetMonth and fly away!
    if targetMonth != 0:
        monthText = ''
        for filename in os.listdir(cwd):
            if filename.endswith('output.txt'):
                monthText = monthText + filename + '\n'
                filepath = os.path.join(cwd,filename)

                with open(filepath, 'r') as file:
                    for line in file:
                        if line.startswith(str(targetMonth)):
                            monthText = monthText + line + '\n'

        #Create an output file for the month's report
        outputFile = months[targetMonth-1] + 'Output.txt'
        with open(outputFile, 'w') as file:
            file.write(monthText)
