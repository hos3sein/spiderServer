#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from aiohttp import web
# import web
from getdata import views
import socketio
# from wsgi import app
import time
from interval_timer import IntervalTimer
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# exchange = os.getenv("APIKEY")
currentDateAndTime = datetime.now()


sio = socketio.AsyncServer(cors_allowed_origins="*" , async_mode='aiohttp')
app = web.Application()
sio.attach(app)

lastStatus = ['no last status ...']
chatHistory = []
validIp = ['62.60.164.218' , '91.107.153.25']
bossess = {'hossein' : ['V816.0.2.0.UGPMIXM'] , 'elham' : ['A515FXXU5GVK6'] , 'laptop' : ['98-59-7A-B3-41-4C']}
bossessId = {'hossein' : '' , 'elham' : '' , 'laptop' : '' , 'spot' : '' , 'futures' : '' , 'analyzor' : '' , 'position' : ''}
waitedMessage = {'hossein' : [] , 'elham' : []}
Status = ['give' , 'me' , 'a' ,  'last' ,'status' , 'give' , 'me' , 'last', 'status' , 'tell', 'me' ,'last', 'status' , 'whats', 'the', 'last', 'status' , 'tell' , 'me' , 'the' , 'last' , 'status' , 'last' , 'status' , 'whats' , 'spider' , 'status' , 'whats' , 'status']
sendMessage = ['say' , 'tell' , 'elie' , 'ellie' , 'ely' , 'eli' , 'elham' , 'alham' , 'to' ,'Say' , 'Tell' , 'Elie' , 'Ellie' , 'Ely' , 'Eli' , 'Elham' , 'Alham' , 'To' , 'hossein' , 'Hossein' , 'Hussain' , 'hussain' , 'hussein' , 'Hissein' ]
darya = ['shut' , 'Shut' , 'down' , 'Down' , 'sleep' , 'Sleep' , 'lock' , 'Lock' , 'wake' , 'Wake' , 'Up' , 'up' , 'it' , 'It' , 'shutdown' , 'Shutdown' , 'wakeup' , 'Wakeup']
darya2 = ['daria' , 'Daria' , 'Dario' , 'dario' , 'darya' , 'Darya' , 'laptop' , 'system' , 'Laptop' , 'System' , 'laptob' , 'Laptob' , 'my laptop' , 'My laptop' , 'my laptob' , 'My laptop']
identify = ["i'm" , 'i' , 'I' , "I'm" , 'i am' , 'I am' , 'my' , 'My' , 'name' , 'Name' , 'is' , 'Is' , 'am' , 'Am' , 'every' , 'Every' , 'buddy' , 'Buddy' , 'call' , 'Call' , 'me' , 'Me']
waitForAnswer = {'wait' : {'id' : '' , 'question' : ''}}
toDoList = ['what' , 'is' , 'Is' , 'What' , 'my' , 'My' , 'Todo' , 'todo' ,'To-do' , 'to-do' , 'To' , 'to' , 'do' , 'Do' , 'list' , 'List' , 'give' , 'Give' , 'me' , 'Me' , 'a' , 'The' , 'tell' , 'Tell' , 'for' , 'For' , 'can' , 'Can' , 'i' , 'I' ]
onlines = ['who' , 'Who' , 'who is' , 'Who is' , 'is' , 'Is' , 'online' , 'Online' , "who's" , "Who's" , 'Whose' , 'whose' , 'get' , 'Get' , 'Me' , 'me']
balance = ['my' , 'My' , 'balance' , 'Balance' , 'give' , 'Give' , 'me' , 'Me' , 'waht' , 'What' , 'is' , 'Is' , 'how' , 'How' , 'much' , 'Much' , 'money' , 'Money' , 'i' , 'I' , 'have' , 'Have' , 'check' , 'Check']

waitForPasswor = 0

doinglist = []


# 'HTTP_MACADDRESS': 'A515FXXU5GVK6'

def balanceChecker(message):
    text = message.split(' ')
    counter = 0
    for i in text:
        if i in balance:
            counter += 1
    if (counter == len(text)):
        return True



def dolist(message):
    text = message.split(' ')
    counter = 0
    for i in text:
        if i in toDoList:
            counter += 1
    if ((counter/len(text))*100 >= 60):
        return True


def onlineChecker(message):
    text = message.split(' ')
    counter = 0
    for i in text:
        if i in onlines:
            counter += 1
    if ((counter/len(text))*100 >= 60):
        return True


def Darya(message):
    message = message.split(' ')
    command = ''
    for i in message:
        if i in darya:
            command += ' ' + i
    print(command)
    return command

def checkStatus(message):
    text = message.split(' ')
    counter = 0
    for i in text:
        if i in Status:
            counter += 1
    if ((counter/len(text)*100) >= 80):
        for i in text:
            if i in Status:
                pass
            else:
                Status.append(i)
        return True



def checkForDarya(message):
    checker = False
    counter = 0
    for i in darya2:
        if i in message:
            checker = True

    return checker


def ident(message):
    text = message.split(' ')
    name = ''
    for i in text:
        if i in identify:
            pass;
        else:
            name += ' ' + i
    return (name)


def sCounter(message , wordList):
    tex = message.split(' ')
    print('tes>>>>' , tex)
    counter = 0
    search = ''
    for i in tex :
        if i in wordList:
            counter += 1
        else:
            search +=' ' + i
    print('messageeeeeeeeeeeee' , search)
    return search




@sio.on('connect')
async def connect(sid, environ , headers):
    print('connected deviced' , sid)
    IP = environ['HTTP_MACADDRESS']
    print('ip connection' , environ['HTTP_MACADDRESS'])
    if (IP in bossess['hossein']):
        bossessId['hossein'] = sid
        print(bossessId)
        
        await sio.emit('answer', {'data' :  f'connection is true for just you {environ['HTTP_X_REAL_IP']}' , 'message' : f'well come back hossein!!!'} , room = sid)
        if (len(waitedMessage['hossein']) != 0):
                for i in range(len(waitedMessage['hossein'])):
                    await sio.emit('answer', {'data' :  f'you have unread message from elham => {waitedMessage['hossein'][i]}' , 'message' : 'you have unread message from hosseind' +'  ' +  waitedMessage['hossein'][i] } , room = sid)
                    
        await sio.emit('backData' ,{'data' :f'>>>connection reset with ip :{IP} => last status => {lastStatus[-1]}'} , room=sid)


    elif (IP in bossess['elham']):
        bossessId['elham'] = sid
        print(bossessId)
        await sio.emit('answer', {'data' :  f'elham is connected to server with ip : {environ['HTTP_X_REAL_IP']}' , 'message' : 'well come back elham!!!'} , room = sid)
        if (len(waitedMessage['elham']) != 0):
                for i in range(len(waitedMessage['elham'])):
                    await sio.emit('answer', {'data' :  f'you have unread message from hossein => {waitedMessage['elham'][i]}' , 'message' : 'you have unread message from elhamd' +'  '+ waitedMessage['elham'][i]} , room = sid)
                    
        await sio.emit('backData' ,{'data' :f'>>>connection reset => last status => {lastStatus[-1]}'} , room=sid)
    else:
        print('is this test>>>')
        waitForAnswer[sid] = {'question' : 'identify'}
        waitForAnswer['wait'] = {'id' : sid , 'question' : 'identify'}

        print(waitForAnswer)
        await sio.emit('answer', {'data' :  f'i dont know you , please identify yourself' , 'message' : 'i dont know you , please identify yourself'} , room = sid)



@sio.on('connect' , namespace='/system')
async def laptopConnection(sid , environ):
    print('laptop successfully connected')
    IP = environ['HTTP_MACADDRESS']
    if (IP in bossess['laptop']):
        bossessId['laptop'] = sid
        print(bossessId)
        # 
        await sio.emit('answer' , {'data' : 'i have been conneted to your laptop' , 'message' : 'i have been conneted to your laptop'} , room=bossessId['hossein'])
    else:
        # 
        await sio.emit('answer' , {'data' : 'some one want to connect me from your pc' , 'message' : 'isome one want to connect me from your pc'} , room=bossessId['hossein'])


@sio.on('connect' , namespace='/spot')
async def laptopConnection(sid , environ):
    print('spot successfully connected')
    bossessId['spot'] = sid
    print(bossessId)
    await sio.emit('answer' , {'data' : 'i have been conneted to spot robot' , 'message' : 'i have been conneted to spot robot'} , room=bossessId['hossein'])


@sio.on('connect' , namespace='/futures')
async def laptopConnection(sid , environ):
    print('futures successfully connected')
    bossessId['futures'] = sid
    print(bossessId)
    await sio.emit('answer' , {'data' : 'i have been conneted to futures robot' , 'message' : 'i have been conneted to futures robot'} , room=bossessId['hossein'])


@sio.on('connect' , namespace='/analyzor')
async def laptopConnection(sid , environ):
    print('analyzor successfully connected')
    bossessId['analyzor'] = sid
    print(bossessId)
    await sio.emit('answer' , {'data' : 'i have been conneted to analyzor' , 'message' : 'i have been conneted to analyzor'} , room=bossessId['hossein'])


@sio.on('connect' , namespace='/position')
async def laptopConnection(sid , environ):
    print('position robot successfully connected')
    bossessId['position'] = sid
    print(bossessId)
    await sio.emit('answer' , {'data' : 'i have been conneted to position robot' , 'message' : 'i have been conneted to position robot'} , room=bossessId['hossein'])


@sio.on('disconnect')
async def disconnect(sid):
    if (bossessId['hossein'] == sid):
        print('hossein disconnected')
        bossessId['hossein'] = ''
    elif(bossessId['elham'] == sid):
        print('elham disconnected')
        await sio.emit('answer' , {"data" : 'elham desconnected' , 'message' : 'elham disconnected'} , room=bossessId['hossein'])
        bossessId['elham'] = ''
    print(f'disconnect device with ip : ' , sid)



@sio.on('disconnect' , namespace='/system')
async def disconnect(sid):
        bossessId['laptop'] = ''
        await sio.emit('answer' , {"data" :f'laptop left the server....' , 'message' : f'laptop  left the server....'} , room=bossessId['hossein'])
        print(f'{'laptop'} left the server....')


@sio.on('disconnect' , namespace='/spot')
async def disconnect(sid):
        bossessId['spot'] = ''
        await sio.emit('answer' , {"data" :f'spot bot left the server....' , 'message' : f'spot bot left the server....'} , room=bossessId['hossein'])
        print(f'spot left the server....')


@sio.on('disconnect' , namespace='/futures')
async def disconnect(sid):
        bossessId['futures'] = ''
        await sio.emit('answer' , {"data" :f'futures bot left the server....' , 'message' : f'futures bot left the server....'} , room=bossessId['hossein'])
        print(f'futures bot left the server....')


@sio.on('disconnect' , namespace='/analyzor')
async def disconnect(sid):
        bossessId['analyzor'] = ''
        await sio.emit('answer' , {"data" :f'analyzor bot left the server....' , 'message' : f'analyzor bot left the server....'} , room=bossessId['hossein'])
        print(f'analyzor bot left the server....')

@sio.on('disconnect' , namespace='/position')
async def disconnect(sid):
        bossessId['position'] = ''
        await sio.emit('answer' , {"data" :f'position bot left the server....' , 'message' : f'position bot left the server....'} , room=bossessId['hossein'])
        print(f'position bot left the server....')



@sio.on('newFile' , namespace='/system')
async def fileChange(sid , data):
    await sio.emit('answer' , {'data' : data['data'] , 'message' : 'new file added to system , i sent the root and file name to you'})


@sio.on('message')
async def chat(sid , data):
    global waitForPasswor
    if(bossessId['hossein'] != sid and bossessId['elham'] != sid):
        if(waitForAnswer['wait']['id'] == ''):
            valid = False
            for i in bossessId.keys():
                if bossessId[i] == sid:
                    valid = True
            if (valid != True):
                await sio.emit('answer' , {'data' : f'someone with sid {sid} want to speak with me' , 'message' : f'someone with sid {sid} want to speak with me'} , room=bossessId['hossein'])
                await sio.emit('answer' , {'data' : f'you are not allowed to speak with me' , 'message' : f'you are not allowed to speak with me'} , room=sid)
        elif (waitForAnswer['wait']['id'] != ''):
            if(waitForAnswer['wait']['id'] == sid):
                if (waitForAnswer['wait']['question'] == 'identify'):
                    name = ident(data['data'])
                    bossessId[name] = sid
                    waitForAnswer['wait']['id'] = ''
                    waitForAnswer['wait']['question'] = ''
                    await sio.emit('answer' , {'data' : f'nice to meet you {name}' , 'message' : f'nice to meet you {name}'} , room=sid)
            else:
                await sio.emit('answer' , {'data' : f'you are not allowed to speak with me' , 'message' : f'you are not allowed to speak with me'} , room=sid)
    

    elif(waitForPasswor == 1 and 'pass' in data['data']):
        print (data['data'])
        if (data['data'] == 'pass 2420685' or data['data'] == 'pass2420685'):
            waitForPasswor = 0
            exchange = os.getenv("APIKEY")
            br = views.broker(exchange)
            eth = br.balance('eth')
            usdt = br.balance('usdt')
            ETH = "{:.3f}".format(float(eth))
            USDT = "{:.2f}".format(float(usdt))
            await sio.emit('answer' , {'data' : f'usdt : {usdt} , eth : {eth}' , 'message' : f'we have {ETH} etherium  , and ,  {USDT} theter on our broker' })
        else :
            await sio.emit('answer' , {'data' : 'acccess denied' , 'message' : f'access denied' })
    

    elif (waitForPasswor == 1 and 'pass' not in data['data']):
        waitForPasswor = 0
        await sio.emit('answer' , {'data' : 'acccess denied' , 'message' : f'access denied' })


    elif(balanceChecker(data['data']) == True):
        waitForPasswor = 1 
        await sio.emit('answer' , {'data' : '' , 'message' : f'please Confirm access level' })
    
    
    elif(onlineChecker(data['data']) == True):
        o = ''
        onlinepeople = [x for x in bossessId.keys() if bossessId[x] != '']
        for i in onlinepeople:
            o += ',' + i
        await sio.emit('answer' , {'data' : o , 'message' : f'{o} are online' })

    elif (dolist(data['data']) == True):
        if (len(doinglist) == 0):
            await sio.emit('answer' , {'data' : f'you have no task to do now' , 'message' : f'you have no task to do now'} , room=sid)
        else:
            for i in doinglist:
                await sio.emit('answer' , {'data' : f'{i}' , 'message' : f'{i}'} , room=sid)
                
 
    elif (checkForDarya(data['data']) == True):
        command = Darya(data['data'])
        if (bossessId['laptop'] == ''):
            await sio.emit('answer' , {'data' : f'sorry boss , your laptop is not online' , 'message' : f'sorry boss , your laptop is not online'} , room=sid)
        else:
            await sio.emit('laptop' , {'data' : command} , namespace='/system' , room=bossessId['laptop'])
            await sio.emit('answer' , {'data' : f'system successfully {command}' , 'message' : f'system successfully {command}'} , room=sid)

    elif('say to' in data['data']):
        message = sCounter(data['data'] , sendMessage)
        if (sid == bossessId['hossein']):
            if (bossessId['elham'] != ''):
                await sio.emit('answer' , {'data' : message , 'message' : message} , room=bossessId['elham'])
            else:
                waitedMessage['elham'].append(message)
                print(waitedMessage)
                await sio.emit('answer' , {'data' : 'elham is not online' , 'message' : 'elham is not online'} , room=sid)
        elif(sid == bossessId['elham']):
            if (bossessId['hossein'] != ''):
                await sio.emit('answer' , {'data' : message , 'message' : message} , room=bossessId['hossein'])
            else:
                waitedMessage['hossein'].append(message)
                print(waitedMessage)
                await sio.emit('answer' , {'data' : 'hossein is not online' , 'message' : 'hossein is not online'} , room=sid)
    elif('tell to' in data['data']):
        message = sCounter(data['data'] , sendMessage)
        if (sid == bossessId['hossein']):
            if (bossessId['elham'] != ''):
                await sio.emit('answer' , {'data' : message , 'message' : message} , room=bossessId['elham'])
            else:
                waitedMessage['elham'].append(message)
                print(waitedMessage)
                await sio.emit('answer' , {'data' : 'elham is not online' , 'message' : 'elham is not online'} , room=sid)
        elif(sid == bossessId['elham']):
            if (bossessId['hossein'] != ''):
                await sio.emit('answer' , {'data' : message , 'message' : message} , room=bossessId['hossein'])
            else:
                waitedMessage['hossein'].append(message)
                print(waitedMessage)
                await sio.emit('answer' , {'data' : 'hossein is not online' , 'message' : 'hossein is not online'} , room=sid)
    
    elif(checkStatus(data['data']) == True):
        await sio.emit('answer' , {'data' : lastStatus[-1] , 'message' : lastStatus[-1]} , room=sid)
    
    else:
        print('chat activate')
        chatHistory.append(data)
        print(data)
        answer = views.NLP(data['data'])
        print('answer' , answer)
        await sio.emit('answer' , {'data' : answer , 'message' : answer} , room=sid)



@sio.on('get')
async def currency(sid):
    # here we should make data ready for emiting
    # currenciesData = views.dataReader()
    # print (currenciesData)
    d = lastStatus[::-1]
    history = d[::50]
    await sio.emit('history' , {'data' : d} , room = sid)
    print('data already sent')


@sio.on('new message' , namespace='/futures')
async def currency(sid , data):
     #here we should make data ready for emiting
     #currenciesData = views.dataReader()
     #print (currenciesData)
     print('data refreshed from spider' , data)
     lastStatus.append(data['data'])
     await sio.emit('backData', {'data' : data['data']})
     #print('data already sent')


@sio.on('analyzor' , namespace='/analyzor')
async def analyzor(sid , data):
     print('new data from spider analyzor>>>' , data)
     lastStatus.append(data['data'])
     await sio.emit('backData2' , {'data' : data['data']})


@sio.on('spot' , namespace='/spot')
async def analyzor(sid , data):
     print('new data from spider analyzor>>>' , data)
     lastStatus.append(data['data'])
     await sio.emit('answer' , {'data' : 'new message from spot recieved' , 'message' : f'new message from spot , {data['data']}'})
     await sio.emit('backData2' , {'data' : data['data']})


@sio.on('position' , namespace='/position')
async def analyzor(sid , data):
     print('new data from spider analyzor>>>' , data)
     lastStatus.append(data['data'])
     await sio.emit('backData2' , {'data' : data['data']})




# @sio.on('get-currency-data')
# async def currency(sid , data):
#     # here we should make data ready for emiting
#     # print (data)
#     currenciesData = views.dataReader()
#     # print (currenciesData)
#     dataLen = data['number']+1
#     if ((dataLen*10) > len(currenciesData)):
#         await sio.emit('page', {'status' : 'end' , 'data' : []})
#     else:
#         await sio.emit('page', {'status' : 'onGoing' , 'data' : currenciesData[:dataLen*10]})
#     # print('data already sent')



def main():
   
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currencyData.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    


if __name__ == '__main__':  
    # main()
    web.run_app(app , host='localhost', port=4000)
