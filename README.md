# Workout Application Backend

A Flask REST API for tracking workouts and the exercises in them, built with Flask, SQLAlchemy and Marshmallow.

## Description

Personal trainers can create workouts and reusable exercises, then add exercises to workouts with reps, sets or duration. Exercises can be reused across many workouts through a join table (`WorkoutExercise`). The API validates data at three levels: table constraints, model validations and schema validations.

## Installation

Requires Python 3.8+ and Pipenv.

```bash
git clone https://github.com/margretmiranda-ai/workout-app-backend.git
cd workout-app-backend
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade head
python seed.py
```

## Run

```bash
cd server
flask run --port 5555
```

or `python app.py`. The API is served at `http://localhost:5555`.

## Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show a workout with its exercises, including reps, sets and duration |
| POST | `/workouts` | Create a workout (`date`, `duration_minutes`, `notes`) |
| DELETE | `/workouts/<id>` | Delete a workout and its workout exercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show an exercise and the workouts it appears in |
| POST | `/exercises` | Create an exercise (`name`, `category`, `equipment_needed`) |
| DELETE | `/exercises/<id>` | Delete an exercise and its workout exercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout (`reps`, `sets`, `duration_seconds`) |

## Validations

- **Table constraints:** unique exercise name, non-null fields, and check constraints for positive duration, reps and sets.
- **Model validations:** `@validates` on exercise name and category, workout duration, and reps, sets and duration seconds.
- **Schema validations:** Marshmallow length and range rules, a blank-name check, and a rule requiring at least one of reps, sets or duration.

## Tests

From `server/`, run `python seed.py` and then `python check_all.py`. It checks the seed data, relationships, validations and every endpoint, and prints PASS or FAIL for each.
