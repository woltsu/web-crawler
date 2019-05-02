import socket, select, types, os, errno

class SchedulerClient():
    def __init__(self):
        # Default hostname
        HOST = "127.0.0.1"

        # Check if host has some specific hostname
        if "HOST" in os.environ:
            HOST = os.environ["HOST"]

        # Default port
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

        # Prepare data
        message = b"F####"
        res = b""

        # Begin data exchange
        while True:
            # Get sockets
            readable, writable, _ = select.select([self.sock], [self.sock], [self.sock])
            flag = False

            # If message hasn't been completely sent yet
            if message:
                # Check if socket is ready to write
                for w in writable:
                    # Send message to the scheduler server
                    sent_data = w.send(message)
                    message = message[sent_data:]

            # Check if socket is ready to read
            for r in readable:
                # Receive data
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
        # IPv4 TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.sock.connect_ex(self.server_addr)

        # Set socket to be non-blocking
        self.sock.setblocking(0)

    def close_connection(self):
        self.sock.close()