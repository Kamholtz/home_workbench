import uvicorn
from app.workbench_web import app

# pipenv run uvicorn main:app --reload --host 0.0.0.0
if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="localhost", port=5000)
