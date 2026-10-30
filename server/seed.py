#!/usr/bin/env python3

from datetime import date

from app import app
from models import *

with app.app_context():

    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    pushups = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    deadlift = Exercise(name="Deadlift", category="Strength", equipment_needed=True)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)
    rowing = Exercise(name="Rowing Machine", category="Cardio", equipment_needed=True)
    db.session.add_all([pushups, squats, deadlift, running, rowing])
    db.session.commit()

    print("Seeding workouts...")
    w1 = Workout(date=date(2026, 10, 20), duration_minutes=45, notes="Upper body focus")
    w2 = Workout(date=date(2026, 10, 22), duration_minutes=30, notes="Cardio day")
    w3 = Workout(date=date(2026, 10, 25), duration_minutes=60, notes="Full body")
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print("Seeding workout exercises...")
    entries = [
        WorkoutExercise(workout=w1, exercise=pushups, reps=15, sets=3),
        WorkoutExercise(workout=w1, exercise=deadlift, reps=8, sets=4),
        WorkoutExercise(workout=w2, exercise=running, duration_seconds=1200),
        WorkoutExercise(workout=w2, exercise=rowing, duration_seconds=600),
        WorkoutExercise(workout=w3, exercise=squats, reps=12, sets=4),
        WorkoutExercise(workout=w3, exercise=pushups, reps=20, sets=3),
        WorkoutExercise(workout=w3, exercise=running, duration_seconds=900),
    ]
    db.session.add_all(entries)
    db.session.commit()

    print("Done seeding!")