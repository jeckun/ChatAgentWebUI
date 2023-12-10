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