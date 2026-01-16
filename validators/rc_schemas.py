# validators/rc_schemas.py
from marshmallow import Schema, fields

class RCDeleteSchema(Schema):
    reason = fields.String(required=False)
