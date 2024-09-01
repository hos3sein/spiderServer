from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pandas as pa
from bs4 import BeautifulSoup
import requests, json, lxml
import csv
import json
import random
import requests
def index(request):
    return HttpResponse("test pass!!!!!!!!")


def no(request):
    return HttpResponse("no route test pass!!!!!!")


def getAllData(request):
    data = dataReader()
    return HttpResponse(data)


# hello = ['hello' , 'hey' , 'are you there?' , 'wake up']
# helloAnswer = ['hello grandPa' , 'hi' , 'im here' , 'hey, whats up?']
goodSpeech = ['whats up' , 'how are you baby?' , 'how going on?' , 'are you ok?' , 'are you good?']
goodSpeechAnswer = ['im good!' , 'im good!what about you?' , 'i cant feel anything!' , 'doesnt matter!']
toDo = ['give me a price' , 'give me a status of spider' , 'check the spider' , 'whats the marker status' , 'whats the rsi']
speaking = ['tell me about yourself' , 'who are you??']
search = ['search about ']

hello = ['hello' , 'hi' , 'how' , 'are' , 'you' , 'whats' , 'app' , 'App' , 'friend' , 'boy' , 'boddy' ,'Hello' , 'Hi' , 'How' , 'Are' , 'You' , 'Whats' , 'app' , 'App' , 'Friend' , 'Boy' , 'Boddy' ]

word = {'hello' : ['hi' , 'whatsApp' , 'hello sir, wellcome back' , 'hello again']}

searchTitles = ['tell' , 'talk' , 'Talk' , 'Tell' , 'say' , 'Say' , 'Me' , 'me' ,'for' , 'For' , 'to' , 'To' , 'about' , 'About' , 'can' , 'Can' , 'you' , 'You' , 'search' , 'Search']


def counter(message):
    text = message.split(' ')
    counter = 0
    for i in text:
        if i in hello:
            counter+=1

    if ((counter/len(text)*100) >= 80):
        ran = random.randint(0 , len(word['hello'])-1)
        return(word['hello'][ran])





def sCounter(message):
    tex = message.split(' ')
    counter = 0
    search = ''
    for i in tex : 
        if i in searchTitles:
            counter += 1
        else:
            search = i
    return search



def NLP(message):
    if ('search' in message):
        searchT = sCounter(message)
        return f"i can't search about {searchT} now , please wait"
    elif('tell me' in message):
        searchT = sCounter(message)
        return f"i can't search about {searchT} now , please wait"
    elif('talk' in message):
        searchT = sCounter(message)
        return f"i can't search about {searchT} now , please wait"
    elif ('hello' in message):
        return counter(message)
    elif(message in goodSpeech):
        rand = random.randint(0, len(goodSpeechAnswer)-1)
        return goodSpeechAnswer[rand]
    elif (message in toDo):
        return ('im not sure i can do this for now , give me more time!!')
    # elif(message == 'how is going on')
    elif (message in speaking):
        return ('im a assistant that developed by hossein and elham for helping them but im still under the developing mode')
    elif(message == ''):
        return ('i cant hear you sir')
    
    else:
        return ('i cant understand what you mean...')
    




def finalSearch(url):
    # Making a GET request
    import requests
    from bs4 import BeautifulSoup
    # Making a GET request
    r = requests.get(url)
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('title')
    body = soup.find('body')
    # s = soup.find('p')
    content = body.find_all('p')
    allData = []
    # print(content[0])
    for i in content:
        # print(i.string)
        i = i.string
        if (i != None):
            allData.append(i)

    return(allData)





class broker:
    def __init__(self , token):
        # self.token = token
        self.header = f"Token {token}"
        self.loginUrl = 'https://api.nobitex.ir/auth/login/'
        self.profileUrl = 'https://api.nobitex.ir/users/profile'
        self.balanceUrl = "https://api.nobitex.ir/users/wallets/balance"
        self.positionUrl = 'https://api.nobitex.ir/market/orders/add'
        self.orders = 'https://api.nobitex.ir/market/orders/list?srcCurrency=btc&dstCurrency=usdt&details=2&status=all&tradeType=spot'
        self.profit = 'https://api.nobitex.ir/users/portfolio'
    
    def profile(self):
        user = requests.get(self.profileUrl ,  headers= {"Authorization" : self.header })
        return (user.json())

    

    def getProfit(self , time):
        match time:
           case 'weekly':
                url = f'{self.profit}/last-week-daily-total-profit'
                data =  requests.post(url , headers = {"Authorization" : self.header })
                return (data.json())
           case 'monthly':
                url = f'{self.profit}/last-month-total-profit'
                data =  requests.post(url , headers = {"Authorization" : self.header })
                truelyData = {'totalProfit' : data.json()['total_profit'] , 'totalPercent' : data.json()['total_profit_percentage']}
                return (truelyData)
            

        #    case 'all':
        #         print('hello')
            



    def balance(self , currency):
        data = {"currency":currency}
        balance = requests.post(self.balanceUrl , headers= {"Authorization" : self.header } , data=data)
        print(balance.json())
        data = balance.json()
        return (data['balance'])



    def allOrders(self):
        data = requests.get(self.orders , headers= {"Authorization" : self.header } )
        return data.json()
   
    def makePosition(self , type , amount):
        price = 0
        amount = 0
        if (type == 'buy'):
            data = {"type":'buy' , "srcCurrency":"usdt" , "dstCurrency":"eth" , "amount":amount , "execution" : 'market' , "price":price }
            return (data.json())
        elif (type == 'sell'):
            data = {"type":'sell' , "srcCurrency":"eth" , "dstCurrency":"usdt" , "amount":amount , "execution" : 'market' , "price":price }
            return (data.json())












# token = 'dcb32a645496b0b5ba606467741322caae383e61'
# header = "Authorization: Token yourTOKENhereHEX0000000000"
# UserAgent = 'TraderBot/spider'


# #################################################################

# login = 'https://api.nobitex.ir/auth/login/'


# body = {'username' : '09229055682'  , }


# profile = 'https://api.nobitex.ir/users/profile'


# # profile = requests.get(profile , headers={"Authorization": "Token dcb32a645496b0b5ba606467741322caae383e61"})
# # print(profile.json())

# #########################################################################

# balance = "https://api.nobitex.ir/users/wallets/balance"

# body2 = {"currency":"usdt"}

# # balance = requests.post(balance , headers={"Authorization": "Token dcb32a645496b0b5ba606467741322caae383e61"} , data=body2)
# # print(balance.json())

# ##########################################################################3





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

    page_limit = 4         # page limit if you don't need to fetch everything
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
        
            try:
                search = finalSearch(links)
                data.append(search)
            except:
                print('error')
        
        # stop loop due to page limit condition
        if page_num == page_limit:
            break
        # stop the loop on the absence of the next page
        if soup.select_one(".d6cvqb a[id=pnnext]"):
            params["start"] += 10
        else:
            break
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    body = ''
    for i in data:
        for j in i:
            body.join(str(x) for x in j)
    return (body)





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
