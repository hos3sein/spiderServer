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


currentDateAndTime = datetime.now()


sio = socketio.AsyncServer(cors_allowed_origins="*" , async_mode='aiohttp')
app = web.Application()
sio.attach(app)

lastStatus = ['no last status ...']
chatHistory = []

bossess = {'hossein' : ['37.44.57.166' , '94.24.18.124'] , 'elham' : ['5.114.64.88']}
bossessId = {'hossein' : '' , 'elham' : ''}
waitedMessage = {'hossein' : [] , 'elham' : []}
Status = ['give me a last status' , 'give me last status' , 'tell me last status' , 'whats the last status' , 'tell me the last status' , 'last status' , 'whats spider status' , 'whats status']
sendMessage = ['say' , 'tell' , 'elie' , 'ellie' , 'ely' , 'eli' , 'elham' , 'alham' , 'to' ,'Say' , 'Tell' , 'Elie' , 'Ellie' , 'Ely' , 'Eli' , 'Elham' , 'Alham' , 'To' , 'hossein' , 'Hossein' , 'Hussain' , 'hussain' , 'hussein' , 'Hissein' ]
darya = ['shut' , 'Shut' , 'down' , 'Down' , 'sleep' , 'Sleep' , 'lock' , 'Lock' , 'wake' , 'Wake' , 'Up' , 'up' , 'it' , 'It']
darya2 = ['daria' , 'Daria' , 'darya' , 'Darya' , 'laptop' , 'system' , 'Laptop' , 'System' , 'laptob' , 'Laptob' , 'my laptop' , 'My laptop' , 'my laptob' , 'My laptop']


def Darya(message):
    message = message.split(' ')
    command = ''
    for i in message:
        if i in darya:
            command += ' ' + i
    print(command)
    return command



def checkForDarya(message):
    for i in darya2:
        if i in message:
            return True



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
async def connect(sid, environ):
    print('connected deviced' , sid)
    IP = environ['HTTP_X_REAL_IP']
    print('ip connection' , environ['HTTP_X_REAL_IP'])

    if (IP in bossess['hossein']):
        bossessId['hossein'] = sid
        print(bossessId)
        await sio.emit('answer', {'data' :  f'connection is true for just you {environ['HTTP_X_REAL_IP']}' , 'message' : 'well come back hossein!!!'} , room = sid)
        if (len(waitedMessage['hossein']) != 0):
                for i in range(len(waitedMessage['hossein'])):
                    await sio.emit('answer', {'data' :  f'you have unread message from elham => {waitedMessage['hossein'][i]}' , 'message' : 'you have unread message from hosseind' +'  ' +  waitedMessage['hossein'][i] } , room = sid)
        await sio.emit('backData' ,{'data' :f'>>>connection reset with ip :{IP} => last status => {lastStatus[-1]}'})


    elif (IP in bossess['elham']):
        bossessId['elham'] = sid
        print(bossessId)
        await sio.emit('answer', {'data' :  f'elham is connected to server with ip : {environ['HTTP_X_REAL_IP']}' , 'message' : 'well come back elham!!!'} , room = sid)
        if (len(waitedMessage['elham']) != 0):
                for i in range(len(waitedMessage['elham'])):
                    await sio.emit('answer', {'data' :  f'you have unread message from hossein => {waitedMessage['elham'][i]}' , 'message' : 'you have unread message from elhamd' +'  '+ waitedMessage['elham'][i]} , room = sid)
        await sio.emit('backData' ,{'data' :f'>>>connection reset => last status => {lastStatus[-1]}'})


@sio.on('disconnect')
def disconnect(sid):
    if (bossessId['hossein'] == sid):
        print('hossein disconnected')
        bossessId['hossein'] = ''
    elif(bossessId['elham'] == sid):
        print('elham disconnected')
        bossessId['elham'] = ''
    print(f'disconnect device with ip : ' , sid)



@sio.on('message')
async def chat(sid , data):
    if (checkForDarya(data['data']) == True):
        command = Darya(data['data'])
        await sio.emit('laptop' , {'data' : command})
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
    elif(data['data'] in Status):
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


@sio.on('new message')
async def currency(sid , data):
     #here we should make data ready for emiting
     #currenciesData = views.dataReader()
     #print (currenciesData)
     print('data refreshed from spider' , data)
     lastStatus.append(data['data'])
     await sio.emit('backData', {'data' : data['data']})
     #print('data already sent')


@sio.on('analyzor')
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
