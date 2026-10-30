from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(required=True)

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("name cannot be blank.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=1000))


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def require_a_measure(self, data, **kwargs):
        if not any(data.get(k) for k in ("reps", "sets", "duration_seconds")):
            raise ValidationError(
                "Provide at least one of reps, sets or duration_seconds."
            )


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.Nested(WorkoutSchema, many=True, dump_only=True)