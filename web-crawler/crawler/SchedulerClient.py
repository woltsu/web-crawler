import socket, select, types, os, errno

class SchedulerClient():
    def __init__(self):
        # Initialize server address
        HOST = "127.0.0.1"
        if "HOST" in os.environ:
            HOST = os.environ["HOST"]
        PORT = 65432
        self.server_addr = (HOST, PORT)

    def sendUrls(self, urls):
        self.open_connection()

        # Send urls to the scheduler server. Server expects the first character
        # to be the "method", e.g. P = "push" or F = "fetch", and the
        # last 4 characters to be "####".
        self.sock.sendall(b"P" + b",".join(urls) + b"####")

        self.close_connection()

    def getUrl(self):
        self.open_connection()
        message = b"F####"
        res = b""

        # Begin data exchange
        while True:
            # Get sockets
            readable, writable, _ = select.select([self.sock], [self.sock], [self.sock])
            flag = False

            if message:
                # Check if socket is ready to write
                for w in writable:
                    # Send message to the scheduler server
                    sent_data = w.send(message)
                    message = message[sent_data:]

            # Check if socket is ready to read
            for r in readable:
                res += r.recv(1024)
                
                # Messages between the scheduler client and
                # server end with "####"
                if res[len(res) - 4:] == b"####":
                    res = res[:len(res) - 4]
                    # Turn bytes representation into a proper string
                    res = repr(res)[2:(len(repr(res)) - 1)]
                    flag = True
                    break

            # If all data is received, then break from loop
            if flag:
                break
        print("Received url: ", res)
        self.close_connection()
        return res

    def open_connection(self):
        # Setup IPv4 TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect_ex(self.server_addr)
        self.sock.setblocking(0)

    def close_connection(self):
        self.sock.close()