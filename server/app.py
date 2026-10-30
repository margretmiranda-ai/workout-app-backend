from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import *
from schemas import (
    ExerciseSchema, ExerciseDetailSchema,
    WorkoutSchema, WorkoutDetailSchema,
    WorkoutExerciseSchema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()


@app.errorhandler(ValidationError)
def handle_schema_error(err):
    return make_response({"errors": err.messages}, 400)


@app.errorhandler(ValueError)
def handle_model_error(err):
    return make_response({"errors": [str(err)]}, 400)


@app.errorhandler(IntegrityError)
def handle_integrity_error(err):
    db.session.rollback()
    return make_response({"errors": ["Database constraint violated."]}, 409)


def not_found(name):
    return make_response({"error": f"{name} not found"}, 404)


@app.route("/workouts", methods=["GET"])
def get_workouts():
    return make_response(workouts_schema.dump(Workout.query.all()), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return not_found("Workout")
    return make_response(workout_detail_schema.dump(workout), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = workout_schema.load(request.get_json() or {})
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return make_response(workout_schema.dump(workout), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return not_found("Workout")
    db.session.delete(workout)   # cascade removes its WorkoutExercises
    db.session.commit()
    return make_response("", 204)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    return make_response(exercises_schema.dump(Exercise.query.all()), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return not_found("Exercise")
    return make_response(exercise_detail_schema.dump(exercise), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = exercise_schema.load(request.get_json() or {})
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return make_response(exercise_schema.dump(exercise), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return not_found("Exercise")
    db.session.delete(exercise)
    db.session.commit()
    return make_response("", 204)


@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return not_found("Workout")
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return not_found("Exercise")

    data = workout_exercise_schema.load(request.get_json() or {})
    we = WorkoutExercise(workout=workout, exercise=exercise, **data)
    db.session.add(we)
    db.session.commit()
    return make_response(workout_exercise_schema.dump(we), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)