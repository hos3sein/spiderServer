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

sio = socketio.AsyncServer(cors_allowed_origins="*" , async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.on('connect')
async def connect(sid, environ):
    while True:
        await sio.emit('backData', {'data' : 'its test for this  server!!!' })
        time.sleep(50)
    print('connect deviced', sid )
    

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect device' , sid)
 

# @sio.on('get')
# async def currency(sid):
#     # here we should make data ready for emiting
#     currenciesData = views.dataReader()
#     # print (currenciesData)
#     await sio.emit('backData', {'data' : currenciesData })
#     print('data already sent')




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
    web.run_app(app , host='localhost', port=8000)