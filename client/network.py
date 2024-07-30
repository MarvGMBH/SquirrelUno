import socketio
import threading

class GameClient:
    def __init__(self, server_url):
        self.sio = socketio.Client()
        self.server_url = server_url
    
    def _connect(self):
        self.sio.connect(self.server_url)
        self.sio.wait()
        
    def start(self):
        threading.Thread(target=self._connect).start()


if __name__ == '__main__':
    server_url = "http://127.0.0.1:5000"
    client = GameClient(server_url)
    client.start()
    input("stop")