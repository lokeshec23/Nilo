# run_server.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   # import path: module:object
        host="0.0.0.0",   # accessible from network (use "127.0.0.1" for local only)
        port=8000,
        reload=True       # auto-reload on code changes (for development)
    )
