from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class WorkoutIn(BaseModel):
    date: str
    exercise: str

workouts = [
    {"id": 1, "date": "2026-10-10", "exercise": "Bench press"},
    {"id": 2, "date": "2026-10-12", "exercise": "Squat"},
]

@app.get("/")
def root():
    return {"message": "Hello from the workout tracker"}

@app.get("/workouts")
def get_workouts():
    return workouts

@app.post("/workouts")
def add_workout(workout: WorkoutIn):
    new_workout = {
        "id": len(workouts) + 1,
        "date": workout.date,
        "exercise": workout.exercise,
    }
    workouts.append(new_workout)
    return new_workout