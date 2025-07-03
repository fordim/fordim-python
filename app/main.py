from fastapi import FastAPI
from app.api import time_tracker

app = FastAPI()

app.include_router(time_tracker.router, prefix="/time-tracker", tags=["time-tracker"])

@app.get("/")
def root():
    return {"message": "Привет из FastAPI!"}
