from marshmallow import Schema,fields


class PlainTodoSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deadline = fields.DateTime(allow_none=True)
    is_done = fields.Bool(load_default=False)


class TodoUpdateSchema(Schema):
    name = fields.Str()
    deadline = fields.DateTime(allow_none=True)
    is_done = fields.Bool()

class TodoSchema(PlainTodoSchema):
    pass