# validators/discussion_schemas.py
from marshmallow import Schema, fields, validate

class CommentCreateSchema(Schema):
    nc_id = fields.Integer(required=True)
    text = fields.String(required=True, validate=validate.Length(min=1, max=4000))
    parent_id = fields.Integer(required=False)

class VoteSchema(Schema):
    comment_id = fields.Integer(required=True)
    delta = fields.Integer(required=True, validate=validate.OneOf([-1, 1]))
