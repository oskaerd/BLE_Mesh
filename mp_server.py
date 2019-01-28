from multiprocessing.connection import Listener

# client
def child(conn):
    while True:
        msg = conn.recv()
        # this just echos the value back, replace with your custom logic
        conn.send(msg)

# server
def mother(address):
    serv = Listener(address)
    while True:
        try:
            client = serv.accept()
            child(client)
        except EOFError:
            print('lol')
            pass

mother(('', 5000))
