from flask import Flask, request
from flask_socketio import SocketIO

from db import DataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
sio = SocketIO(app, cors_allowed_origins="*") # allow cors for development

db = DataBase()

@sio.event
def connect():
  print(f'connect: {request.sid}', flush=True)

@sio.event
def query_course_info(data):
  global db
  result = {'categories':db.get_categories(),'courses':db.get_courselist()}
  sio.emit('course_info', result, room=request.sid)

@sio.event
def query_course_list(data):
  global db
  sio.emit("course_list_result", db.query_course_list(data), room=request.sid)

@sio.event
def query_course_minprice(data):
  global db
  print(f'{request.sid}: request {data}')
  sio.emit("minprice_result", db.query_course_minprice(data), room=request.sid)

@sio.event
def disconnect():
  print(f'disconnect: {request.sid}', flush=True)

if __name__ == '__main__':
  print('server start', flush=True)
  sio.run(app, host="0.0.0.0") # address binding for Flask server