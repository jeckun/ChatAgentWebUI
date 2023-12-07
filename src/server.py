from threading import Thread
from src.route import app

def server_run():
    app.run(host='0.0.0.0', port=8080, debug=True)

def keep_alive():
    if __name__ == '__main__':
        t = Thread(target=server_run)
        t.start()