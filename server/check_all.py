#!/usr/bin/env python3
from sqlalchemy.exc import IntegrityError
from app import app
from models import *


def check(label, ok):
    print(("PASS  " if ok else "FAIL  ") + label)


def raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


JSON = {"content_type": "application/json"}

with app.app_context():
    # --- Seed data ---
    check("5 exercises seeded", Exercise.query.count() == 5)
    check("3 workouts seeded", Workout.query.count() == 3)
    check("7 workout_exercises seeded", WorkoutExercise.query.count() == 7)

    # --- Relationships ---
    w = Workout.query.first()
    e = Exercise.query.filter_by(name="Running").first()
    check("workout.exercises works", len(list(w.exercises)) >= 1)
    check("exercise.workouts works", len(list(e.workouts)) == 2)
    check("join row belongs to workout and exercise",
          w.workout_exercises[0].workout is w and w.workout_exercises[0].exercise is not None)

    # --- Model validations ---
    check("blank exercise name rejected",
          raises(ValueError, lambda: Exercise(name="  ", category="Cardio", equipment_needed=True)))
    check("negative duration rejected",
          raises(ValueError, lambda: Workout(duration_minutes=-5)))
    check("reps=0 rejected", raises(ValueError, lambda: WorkoutExercise(reps=0)))

    # --- Table constraint ---
    try:
        db.session.add(Exercise(name="Push-ups", category="Strength", equipment_needed=False))
        db.session.commit()
        check("duplicate name blocked by database", False)
    except IntegrityError:
        db.session.rollback()
        check("duplicate name blocked by database", True)

    # --- Endpoints ---
    c = app.test_client()
    r = c.get("/workouts")
    check("GET /workouts 200", r.status_code == 200 and len(r.json) > 0)
    wid = r.json[0]["id"]

    r = c.get(f"/workouts/{wid}")
    check("GET /workouts/<id> has reps/sets data",
          r.status_code == 200 and "workout_exercises" in r.json)

    r = c.get("/exercises")
    check("GET /exercises 200", r.status_code == 200 and len(r.json) > 0)
    eid = r.json[0]["id"]

    r = c.get(f"/exercises/{eid}")
    check("GET /exercises/<id> has workouts",
          r.status_code == 200 and "workouts" in r.json)

    r = c.post("/exercises", json={"name": "Lunges", "category": "Strength", "equipment_needed": False})
    check("POST /exercises 201", r.status_code == 201)
    new_ex = r.json.get("id")
    check("POST /exercises blank name 400",
          c.post("/exercises", json={"name": "", "category": "Strength", "equipment_needed": False}).status_code == 400)
    check("POST /exercises duplicate 409",
          c.post("/exercises", json={"name": "Lunges", "category": "Strength", "equipment_needed": False}).status_code == 409)

    r = c.post("/workouts", json={"date": "2026-11-01", "duration_minutes": 40, "notes": "Test"})
    check("POST /workouts 201", r.status_code == 201)
    new_w = r.json.get("id")
    check("POST /workouts negative duration 400",
          c.post("/workouts", json={"date": "2026-11-01", "duration_minutes": -1}).status_code == 400)

    url = f"/workouts/{new_w}/exercises/{eid}/workout_exercises"
    check("POST add exercise to workout 201", c.post(url, json={"reps": 10, "sets": 3}).status_code == 201)
    check("POST add exercise with no measure 400", c.post(url, json={}).status_code == 400)
    check("POST add exercise bad ids 404",
          c.post("/workouts/9999/exercises/9999/workout_exercises", json={"reps": 5}).status_code == 404)

    check("DELETE /workouts/<id> 204", c.delete(f"/workouts/{new_w}").status_code == 204)
    check("deleted workout now 404", c.get(f"/workouts/{new_w}").status_code == 404)
    check("DELETE /exercises/<id> 204", c.delete(f"/exercises/{new_ex}").status_code == 204)