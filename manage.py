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

bossess = {'hossein' : ['37.44.57.166'] , 'elham' : ['']}


@sio.on('connect')
async def connect(sid, environ):
    print('connected deviced' , sid)
    IP = environ['HTTP_X_REAL_IP']
    print('ip connection' , environ['HTTP_X_REAL_IP'])

    if (IP in bossess['hossein']):
        await sio.emit('answer', {'data' :  f'connection is true for just you {environ['HTTP_X_REAL_IP']}' , 'message' : 'well come back hossein!!!'} , room = sid)
        await sio.emit('backData' ,{'data' :f'>>>connection reset => last status => {lastStatus[-1]}'})


    elif (IP in bossess['elham']):
        await sio.emit('answer', {'data' :  f'elham is connected to server with ip : {environ['HTTP_X_REAL_IP']}' , 'message' : 'well come back elham!!!'} , room = sid)
        await sio.emit('backData' ,{'data' :f'>>>connection reset => last status => {lastStatus[-1]}'})


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect device' , sid)

@sio.on('message')
async def chat(sid , data):
    ipAddress = sid.handshake.address
    print('chat activate')
    chatHistory.append(data)
    print(data)
    answer = views.NLP(data['data'])
    print('answer' , answer)
    await sio.emit('answer' , {'data' : answer , 'message' : answer})


@sio.on('get')
async def currency(sid):
    # here we should make data ready for emiting
    # currenciesData = views.dataReader()
    # print (currenciesData)
    d = lastStatus[::-1]
    history = d[::50]
    await sio.emit('history' , {'data' : d})
    print('data already sent')


@sio.on('new message')
async def currency(sid , data):
     #here we should make data ready for emiting
     #currenciesData = views.dataReader()
     #print (currenciesData)
     print('data refreshed from spider' , data)
     lastStatus.append(data['data'])
     await sio.emit('backData', {'data' : data['data'] })
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
