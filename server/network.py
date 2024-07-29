from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from utils import UIDObject
import threading
import time

class Networking(UIDObject):
    def __init__(self, port):
        super().__init__()
        self.__app = Flask(__name__)
        self.__socketio = SocketIO(self.app)
        self.__connections = {}
        self.__port = port
        self.__events = {}

        self.__socketio.on_event('connect', self.handle_connect)
        self.__socketio.on_event('disconnect', self.handle_disconnect)
        self.__socketio.on_event('message', self.handle_message)

        @self.app.route('/receive_message', methods=['POST'])
        def __receive_message():
            data = request.json
            print(f"Received message from another server: {data['message']}")
            return jsonify({'status': 'received'})

    def __handle_connect(self):
        client_id = request.sid
        self.__connections[client_id] = {'id': client_id}
        print(f'Client {client_id} connected')
        if 'connect' in self.__events:
            for callback in self.__events['connect']:
                callback(client_id)

    def __handle_disconnect(self):
        client_id = request.sid
        if client_id in self.__connections:
            del self.__connections[client_id]
        print(f'Client {client_id} disconnected')
        if 'disconnect' in self.__events:
            for callback in self.__events['disconnect']:
                callback(client_id)

    def __handle_message(self, data):
        client_id = request.sid
        print(f"Received message from {client_id}: {data['message']}")
        emit('message', {'message': f"Server received: {data['message']}"}, room=client_id)
        if 'message' in self.__events:
            for callback in self.__events['message']:
                callback(client_id, data['message'])

    def send_json(self, client_id, data):
        if client_id in self.__connections:
            emit('json', data, room=client_id)
            print(f"Sent JSON to {client_id}: {data}")
        else:
            print(f"Client {client_id} not connected")

    def start_server(self):
        self.__socketio.run(self.__app, port=self.__port, debug=True)
