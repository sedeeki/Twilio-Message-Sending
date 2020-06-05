import os
from twilio.rest import Client
import pandas as pd
from datetime import date
from tabulate import tabulate
import plotly.express as px
import numpy as np

today = str(date.today())
print(today) 



data = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv')
date = data['Date']
allData = [data['Confirmed'],data['Deaths'],data['Recovered'],data['Country']] 
currData = [[],[],[],[],[]]


for i in range(len(allData[0])):
    if (date[i] == '2020-05-13'):
        currData[0].append(date[i])
        currData[1].append(allData[0][i])
        currData[2].append(allData[1][i])
        currData[3].append(allData[2][i])
        currData[4].append(allData[3][i])
        
results = [(currData[0][x],currData[1][x],currData[2][x],currData[3][x],currData[4][x]) for x in range(len(currData[0]))]
table = tabulate(results, headers=["Date","Confirmed","Deaths","Recovered","Country"])

usaresults = []
for i in range(len(results)):
    if(results[i][4] == 'US'):
        usaresults.append(results[i][0:4])

string = str(usaresults)


x = str(input("Do you have Twilio account? (Y/N): "))
if (x == 'Y'):
    accID = None
    accID = str(input("Enter acc ID: "))
    auth =  str(input("Enter authentication token: "))
    client = Client('AC7bad362e228267c60a44ea86aa440e89','7fe90ef8d9814b77b145062f07dcf190')
    
    message = client.messages.create(from_='+12058808890',
                          to='+923440518985',
                          body=string)
    
if (x != 'Y' and x != 'N'):
    print("Error: Could not interpret selection")

dataFrame = (date,data['Confirmed'])
x = str(input("Would you like to visualize Corona Cases? (Y/N): "))
if (x == 'Y'):
    confirmed = data['Confirmed']
    total = []
    uDate = date
    uDate = np.unique(uDate)
    for i in uDate:
        total.append(0)
    index = 0
    for i in range(len(date)):
        if (uDate[index] == date[i]):
            total[index] = total[index] + confirmed[i]
        else:
            index = index + 1
            total[index] = total[index] + confirmed[i]
    dict = {}
    dict = {"Last Updated":uDate,"Total Cases":total}
    fig = px.line(dict,x = 'Last Updated', y = 'Total Cases', title='WorldWife Confirmed Covid 19 Cases Over Time')
    fig.show()
if (x != 'Y' and x != 'N'):
    print("Error: Could not interpret selection")
    

print("What statistics would you like to see? Please enter via the format: [Country,Variable]")
print("You may choose any of the following variables (All, confirmed, deaths, recovered")
print("You can also input (All) for country and list statistics by variables (Death, confirmed, recovered")
x = str(input("Or type exit to exit: "))

while(x != "exit"):
    country = ""
    flip = 0
    variable = ""
    for i in range(1,len(x)-1):
        if (flip == 1):
            flip = 2
        if (x[i] == ","):
            flip = 1
        if (flip == 0):
            country = country + x[i]
        if (flip == 2):
            variable = variable + x[i]
    dataset = []
    if (country != "All"):
        for i in range(len(results)):
            if(results[i][4] == country):
                dataset.append([results[i][1],results[i][2],results[i][3]])
        if (variable == 'All'):
            table = tabulate(dataset, headers=["Confirmed","Deaths","Recovered"])
            print(table)
        elif (variable == 'Deaths'):
            print(int(dataset[0][1]))
        elif (variable == 'Confirmed'):
            print(int(dataset[0][0]))
        elif (variable == 'Recovered'):
            print(int(dataset[0][2]))
    else:
        dataset = None
        if (variable == 'All'):
            dataset = [(results[x][1:4]) for x in range(len(results))]
            table = tabulate(dataset, headers=["Confirmed","Deaths","Recovered"])
            print(table)
        elif (variable == 'Deaths'):
            dataset = [(results[x][4],results[x][2]) for x in range(len(results))]
            table = tabulate(dataset, headers=["Deaths"])
            print(table)
        elif (variable == 'Confirmed'):
            dataset = [(results[x][4],results[x][1]) for x in range(len(results))]
            table = tabulate(dataset, headers=["Confirmed"])
            print(table)
        elif (variable == 'Recovered'):
            dataset = [(results[x][4],results[x][3]) for x in range(len(results))]
            table = tabulate(dataset, headers=["Recovered"])
            print(table)

    print("What statistics would you like to see? Please enter via the format: [Country,Variable]")
    print("You may choose any of the following variables (All, confirmed, deaths, recovered")
    print("You can also input (All) for country and list statistics by variables (Death, confirmed, recovered")
    x = str(input("Or type exit to exit: "))






