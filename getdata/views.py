from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pandas as pa
from bs4 import BeautifulSoup
import requests, json, lxml
import csv
import json
import random
def index(request):
    return HttpResponse("test pass!!!!!!!!")


def no(request):
    return HttpResponse("no route test pass!!!!!!")


def getAllData(request):
    data = dataReader()
    return HttpResponse(data)


hello = ['hello' , 'hey' , 'are you there?' , 'wake up']
helloAnswer = ['hello grandPa' , 'hi' , 'im here' , 'hey, whats up?']
goodSpeech = ['whats up' , 'how are you baby?' , 'how going on?' , 'are you ok?' , 'are you good?']
goodSpeechAnswer = ['im good!' , 'im good!what about you?' , 'i cant feel anything!' , 'doesnt matter!']
toDo = ['give me a current price' , 'give me a status of spider' , 'check the spider' , 'whats the marker status' , 'whats the rsi']
speaking = ['tell me about yourself' , 'who are you??']
search = ['search about ']


def NLP(message):
    if ('search' in message):
        message2 = message.split(' ')
        if (message2[0] == 'search'):
            query = message.replace('search' , '' , 1)
            query = message.replace('about' , '' , 1)
            
            resault = search(query)
            return (resault)
        elif(message2[0]!='search'):
            message = message.replace(message2[0] , '' , 1)
            query = message.replace('search' , '' , 1)
            query = message.replace('about' , '' , 1)
            resault = search(query)
            return (resault)
    if (message in hello):
        rand = random.randint(0, len(helloAnswer)-1)
        return helloAnswer[rand]
    if(message in goodSpeech):
        rand = random.randint(0, len(goodSpeechAnswer)-1)
        return goodSpeechAnswer[rand]
    if (message in toDo):
        return ('im not sure i can do this for now , give me more time!!')
    if (message in speaking):
        return ('im a assistant that developed by hossein and elham for helping them but im still under the developing mode')
    



def search(query):
    params = {
        "q": query,          # query example
        "hl": "en",          # language
        "gl": "uk",          # country of the search, UK -> United Kingdom
        "start": 0,          # number page by default up to 0
        #"num": 100          # parameter defines the maximum number of results to return.
    }
    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    page_limit = 10          # page limit if you don't need to fetch everything
    page_num = 0

    data = []

    while True:
        page_num += 1
        print(f"page: {page_num}")
            
        html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, 'lxml')
        
        for result in soup.select(".tF2Cxc"):
            title = result.select_one(".DKV0Md").text
            try:
                print(result.select_one(".lEBKkf span").text)
                snippet = result.select_one(".lEBKkf span").text
            except:
                snippet = None
            links = result.select_one(".yuRUbf a")["href"]
        
            data.append({
            "title": title,
            "snippet": snippet,
            "links": links
            })
        
        # stop loop due to page limit condition
        if page_num == page_limit:
            break
        # stop the loop on the absence of the next page
        if soup.select_one(".d6cvqb a[id=pnnext]"):
            params["start"] += 10
        else:
            break
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return (json.dumps(data, indent=2, ensure_ascii=False))





def dataReader():
    csvFile = open('../../dataBot/data.csv' , 'r')
    jsonFiel = open('dataFile.json' , 'w')
    logoFile = open('../../dataBot/Rdata.json' , 'r')
    logos =  json.load(logoFile)
    fieldsName = ( "" ,"name" , "price" , "prcent_change_1H" , "percent_change_24H")
    readerData = csv.DictReader(csvFile , fieldsName)
    new_data = []
    for row in readerData:
        # print(row)
        # print(row['name'])
        if (row['name'] != 'name'):
            logo = '';
            if (row['name'] in logos):
                logo = logos[row['name']]
                # print(logo)
                row['logo'] = logo
            json.dump(row, jsonFiel)
            jsonFiel.write('\n')
            new_data.append(row)
    return (new_data)
    





    # data = pa.read_csv('../../dataBot/data.csv')
    # print(data)
    # return(data)    