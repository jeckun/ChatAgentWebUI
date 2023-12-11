import uvicorn

def server_run():
    uvicorn.run(
        "src.route:app",
        host="0.0.0.0",
        port=8080,
        log_level="debug",
        reload=True,
    )

if __name__ == '__main__':
    server_run()
