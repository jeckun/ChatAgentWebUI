# from threading import Thread
# from src.route import app

# def server_run():
#     app.run(host='0.0.0.0', port=8080, debug=True)

# def keep_alive():
#     if __name__ == '__main__':
#         t = Thread(target=server_run)
#         t.start()

import uvicorn
from dotenv import load_dotenv

load_dotenv()

def server_run():
    uvicorn.run(
        "src.route:app",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        reload=True,
    )