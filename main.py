import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

DB_FILE = "workouts.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

class WorkoutIn(BaseModel):
    date: str
    exercise: str

@app.get("/")
def root():
    return {"message": "Hello from the workout tracker"}

@app.get("/workouts")
def get_workouts():
    conn = get_connection()
    rows = conn.execute("SELECT id, date, exercise FROM workouts").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/workouts")
def add_workout(workout: WorkoutIn):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO workouts (date, exercise) VALUES (?, ?)",
        (workout.date, workout.exercise),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "date": workout.date, "exercise": workout.exercise}

@app.get("/workouts/{workout_id}")
def get_workout(workout_id: int):
    conn = get_connection()
    row = conn.execute("SELECT id, date, exercise FROM workouts WHERE id=?", (workout_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return dict(row)