from typing import Dict, List

from fastapi import FastAPI
import os

# Definition of Result Alert
base_alert: Dict = {
    "code": "",
    "message": "",
    "result": None
}

app = FastAPI()


@app.get("/")
def hello() -> Dict:
    response = base_alert
    return response


@app.get("/dashboard")
def dashboard() -> Dict:
    response = base_alert
    return {"hello"}
