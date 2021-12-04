import json
import requests
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import logging
import boto3
from botocore.exceptions import ClientError
import os
# d0afb583055c4f17b2028f1ac7c8d4ac



def getGraph(stock, state):
    s3 = boto3.client('s3')
    fileName = "graph_files/" + str(stock) + "-" + str(state) + ".png"
    #fileName = "arn:aws:s3:::eeprojfiles:" + str(stock) + "-" + str(state) + ".png"
    bucket = "eeprojfiles"

    objectName = str(stock).upper() + "-" + str(state).upper() + ".png"
    filepath = ""
    response = s3.upload_file(fileName, bucket, objectName)
    #response = s3.download_file(bucket, objectName, fileName)
    filepath = "https://eeprojfiles.s3.us-west-1.amazonaws.com/" + objectName   
    return filepath

def plotData(c, d, state, ticker):
    plt.plot(c, d, 'ro')
    plt.xlabel('cases')
    plt.ylabel('stock price')
    plt.savefig("graph_files/" + str(ticker) + "-" + str(state) + ".png")
    plt.close();

def getCorrelations(l1, l2):
    sr1 = pd.Series(l1)
    sr2 = pd.Series(l2)
    pearson = int(sr1.corr(sr2, method='pearson') * 100)
    spearman = int(sr1.corr(sr2, method='spearman') * 100)
    kendall = int(sr1.corr(sr2, method='kendall') * 100)
    return (abs(pearson), abs(spearman), abs(kendall))

def getStateNum(name):
    stateDict = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC","AS","GU","MP","PR","UM","VI"]
    try:
        return stateDict.index(name)
    except:
        return -1;


def datamain(state, ticker):
    response = requests.get("https://api.covidactnow.org/v2/states.timeseries.json?apiKey=d0afb583055c4f17b2028f1ac7c8d4ac").json()
    state = state.upper()
    ticker = ticker.upper()

    stateData = response[getStateNum(state)]
    n = 0
    days = []
    cases = []
    d = []
    prevdata = [0]

    while (stateData['actualsTimeseries'][n]["date"] != "2020-03-30"):
        cases.append(stateData['actualsTimeseries'][n]["newCases"])
        days.append(n)
        date = stateData['actualsTimeseries'][n]["date"]
        data = yf.download(ticker, date, stateData['actualsTimeseries'][n + 1]["date"])['Adj Close']
        download_success = [r for r in data if r > 0]
        if(download_success):
            d.append(data[0])
            prevdata = data
        else:
            d.append(prevdata[0])
        
        print(stateData['actualsTimeseries'][n]["date"])
        n += 1

    while(cases[0] == 0):
        d.pop(0)
        cases.pop(0)
        days.pop(0)
    print(len(cases))
    print(len(d))
    plotData(cases, d, state, ticker)
    return getCorrelations(cases, d)






