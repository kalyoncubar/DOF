# validators/action_schemas.py
from marshmallow import Schema, fields, validate

class ActionCreateSchema(Schema):
    rc_id = fields.Integer(required=True)
    assignee_id = fields.Integer(required=True)
    due_date = fields.DateTime(required=False)  # ISO-8601

class ActionTransitionSchema(Schema):
    note = fields.String(required=False, validate=validate.Length(max=500))

class ActionCloseSchema(Schema):
    approved = fields.Boolean(required=True)
    note = fields.String(required=False, validate=validate.Length(max=500))
