import socketio
import threading

class GameClient:
    def __init__(self, server_url):
        self.sio = socketio.Client()
        self.server_url = server_url
        self.connected = False

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.on_message)

    def on_connect(self):
        self.connected = True
        print('Connected to the server')
        self.sio.emit('message', {'message': 'Hello, server!'})

    def on_disconnect(self):
        self.connected = False
        print('Disconnected from server')

    def on_message(self, data):
        print(f"Received message: {data['message']}")

    def send_message(self, message):
        if self.connected:
            self.sio.emit('message', {'message': message})

    def start(self):
        threading.Thread(target=self._connect).start()

    def _connect(self):
        self.sio.connect(self.server_url)
        self.sio.wait()

if __name__ == '__main__':
    server_url = input("Enter the server URL to connect to (e.g., http://localhost:5000): ").strip()
    client = GameClient(server_url)
    client.start()

    while True:
        if client.connected:
            message = input("Enter a message to send to the server: ").strip()
            client.send_message(message)
