import socket

from flask import Flask
import threading

# tcp server
TCP_IP = '127.0.0.1'
TCP_PORT = 5001
BUFFER_SIZE = 20


# flask app
app = Flask(__name__)

light_on = False
thread_on = False
thread = False


def launchServer():
    def run():
        global light_on
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        print("run", flush=True)

        print('waiting for connection', flush=True)
        CONN, addr = s.accept()
        while light_on:
            print('Connection address:', addr, flush=True)
            # Logic Here

        CONN.shutdown(socket.SHUT_RDWR)
        CONN.close()

    global thread
    if thread_on:
        thread = threading.Thread(target=run)
        thread.start()



@app.route('/start')
def start():
    print('starting', flush=True)
    global light_on
    global thread_on
    light_on = True
    thread_on = True
    launchServer()
    return "Started"


@app.route('/stop')
def stop():
    global light_on
    global thread
    global thread_on
    light_on = False
    thread_on = False
    thread.do_run = False
    thread.join()
    return "Stopped"


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8050, use_reloader=False, threaded=True)