from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from utils import UIDObject
import threading
import time

class Networking(UIDObject):
    def __init__(self, port):
        super().__init__()
        self.__app = Flask(__name__)
        self.__socketio = SocketIO(self.__app)
        self.__port = port

        @self.__socketio.on("connect")
        def on_connect(self):
            print(request.sid, "connected")

    def start_server(self):
        self.__socketio.run(self.__app, port=self.__port, debug=True)
