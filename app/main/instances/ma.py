from flask_marshmallow import Marshmallow

ma = Marshmallow()

class BaseSchema(ma.Schema):
    created = ma.AwareDateTime()
    updated = ma.AwareDateTime()

ma.BaseSchema = BaseSchema