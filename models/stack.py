
from marshmallow import Schema, fields


class StackRequest(Schema):
    value = fields.Int(required=True)


class StackResponse(Schema):
    stack_id = fields.Str()
    values = fields.List(fields.Int())
    operands = fields.List(fields.Str())


class AllStacksResponse(Schema):
    data = fields.List(fields.Nested(StackResponse))

