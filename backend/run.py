import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, log_level="debug", port=8888)
