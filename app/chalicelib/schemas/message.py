import uuid
from marshmallow import Schema, fields

class FromSchema(Schema):
    name = fields.Str(require=True)
    email = fields.Email(require=True)

class ToSchema(Schema):
    name = fields.Str(require=True)
    email = fields.Email(require=True)

class MessageSchema(Schema):
    _from = fields.Nested('FromSchema', data_key="from")
    to = fields.Nested('ToSchema', many=True)
    subject = fields.Str(require=True)
    metadata = fields.Raw(required=True)