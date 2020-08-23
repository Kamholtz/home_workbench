import uvicorn

from workbench_web.main import app

# pipenv run uvicorn main:app --reload --host 0.0.0.0
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
