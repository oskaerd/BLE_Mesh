from multiprocessing.connection import Client

c = Client(('localhost', 5000))

c.send('hello')
print('Got:', c.recv())

c.send({'a': 123})
print('Got:', c.recv())