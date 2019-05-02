import socket, types, os, threading
from scheduler import Scheduler

# Global lock that is used when different
# threads write into the result file
fileLock = threading.Lock()

# Update result file with the received links
def update_file(data):
    # Acquire lock
    global fileLock
    fileLock.acquire()
    print("updating file...")
    
    # Update file
    f = open("./data/data.txt", "a+")
    f.write(data)
    f.close()

    # Release lock
    fileLock.release()

def handle_connection(data, conn, scheduler):
    res = b""
    while data:
        res += data
        # Messages between the scheduler client and
        # server end with "####"
        if res[len(res) - 4:] == b"####":
            res = res[:len(res) - 4]
            res = repr(res)[2:(len(repr(res)) - 1)]
            # P = push, F = fetch
            method = res[0]
            # If method is push, then add the received
            # urls to the scheduler and update the result
            # file in a seperate thread
            if method == "P":
                urls = scheduler.feed_urls(res[1:])
                if len(urls) > 0:
                    thread = threading.Thread(target=update_file, args=("\n".join(urls),))
                    thread.start()
            # If the method is fetch, then send the connection
            # the next target url from the scheduler
            elif method == "F":
                conn.send(scheduler.get_next().encode() + b"####")
        # Receive more data if the last characters weren't "####"
        data = conn.recv(1024)  

class SchedulerServer():
    def __init__(self):
        # Determine server address
        HOST = "127.0.0.1"
        if "HOST" in os.environ:
            HOST = os.environ["HOST"]
        PORT = 65432
        self.server_addr = (HOST, PORT)

        # Create a blocking IPv4 TCP server socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.server_addr)
        self.socket.listen()
        print('listening on', (HOST, PORT))
        self.socket.setblocking(1)

        # Initialize scheduler
        if "ROOT_URL" in os.environ:
            self.scheduler = Scheduler.Scheduler(os.environ["ROOT_URL"])
        else:
            print("Please provide a root url.")
            exit(0)

    def start(self):
        # Start server
        try:
            while True:
                # Handle connection requests
                conn, info = self.socket.accept()
                print("accepted connection from", info)
                data = conn.recv(1024)
                if data:
                    # Handle connections in seperate threads
                    thread = threading.Thread(target=handle_connection, args=(data,conn,self.scheduler))
                    thread.start()          
        except Exception as e:
            # In the case of an exception, shut down the server
            print(e)
            self.socket.close()

