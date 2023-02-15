
from marshmallow import Schema, fields


class OperandResponse(Schema):
    stack_id = fields.Str()
    operands = fields.List(fields.Str())


class AllOperandsResponse(Schema):
    data = fields.List(fields.Nested(OperandResponse))
