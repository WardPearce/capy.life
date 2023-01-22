from app.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, log_level="debug", port=8888)
