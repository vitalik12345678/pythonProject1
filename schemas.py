from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=5, max=24), required=True)
    role = fields.Str(validate=validate.Length(min=1, max=24), required=True)
    password = fields.Str(validate=validate.Length(min=5, max=80), required=True)
    location_id = fields.Integer()


class LoginSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=24), required=True)
    password = fields.Str(validate=validate.Length(min=3, max=80), required=True)


class LocationSchema(Schema):
    id = fields.Integer(required=True)
    city = fields.Str(validate=validate.Length(min=1,max=55),required=True)

class ValidateUserFieldsSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=64))
    role = fields.Str(validate=validate.Length(min=5, max=24))
    password = fields.Str(validate=validate.Length(min=5, max=48))
    location_id = fields.List(fields.Nested(LocationSchema))

class MessageSchema(Schema):
    text = fields.Str(validate=validate.Length(min=1, max=80), required=True)
    advertisement_id = fields.Integer(required=True)

class ValidateAdvertisementFieldsSchema(Schema):
    id = fields.Integer()
    title = fields.Str(validate=validate.Length(min=1, max=64), required=True)
    status = fields.Boolean(required=True)

class ValidateMessageFieldsSchema(Schema):
    id = fields.Integer(required=True)

class ValidateAdvertSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=64), required=True)
    status = fields.Boolean(required=True)

class AdvertSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=64), required=True)
    status = fields.Boolean(required=True)
    message = fields.List(fields.Nested(MessageSchema))

class lsitSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=64), required=True)
    status = fields.Boolean(required=True)


class AdvvertList(Schema):
    advertisement_id = fields.List(fields.Nested(AdvertSchema()))

