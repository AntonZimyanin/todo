from todo.main import app
from uvicorn import run

if __name__ == "__main__":
    run("run:app", port=8080, log_level="info")
