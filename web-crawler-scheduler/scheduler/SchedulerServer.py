import socket, types, os, threading
from scheduler import Scheduler

# Global lock that is used when different
# threads write into the result file
lock = threading.Lock()

# Update result file with the received links
def update_file(data):
    # Acquire lock
    global lock
    lock.acquire()
    print("updating file...")
    
    # Update file
    f = open("./data/data.txt", "a+")
    f.write(data)
    f.close()

    # Release lock
    lock.release()

def handle_connection(data, conn, scheduler):
    res = b""
    while data:
        res += data
        if res[len(res) - 4:] == b"####":
            res = res[:len(res) - 4]
            res = repr(res)[2:(len(repr(res)) - 1)]
            # P = push, F = fetch
            method = res[0]
            if method == "P":
                urls = scheduler.feed_urls(res[1:])
                if len(urls) > 0:
                    thread = threading.Thread(target=update_file, args=("\n".join(urls),))
                    thread.start()
            elif method == "F":
                conn.send(scheduler.get_next().encode() + b"####")
        data = conn.recv(1024)  

class SchedulerServer():
    def __init__(self):
        
        HOST = "127.0.0.1"
        if "HOST" in os.environ:
            HOST = os.environ["HOST"]
        PORT = 65432
        self.server_addr = (HOST, PORT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.server_addr)
        self.socket.listen()
        print('listening on', (HOST, PORT))
        self.socket.setblocking(1)

        if "ROOT_URL" in os.environ:
            self.scheduler = Scheduler.Scheduler(os.environ["ROOT_URL"])
        else:
            print("Please provide a root url.")
            exit(0)

    def start(self):
      try:
        while True:
            conn, info = self.socket.accept()
            print("accepted connection from", info)
            data = conn.recv(1024)
            if data:
                thread = threading.Thread(target=handle_connection, args=(data,conn,self.scheduler))
                thread.start()          
      except Exception as e:
        print(e)
        self.socket.close()

