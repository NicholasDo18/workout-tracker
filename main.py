from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from the workout tracker"}

@app.get("/workouts")
def get_workouts():
    return [
        {"id": 1, "date": "2026-10-10", "exercise": "Bench press"},
        {"id": 2, "date": "2026-10-12", "exercise": "Squat"},
    ]