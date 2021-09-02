from marshmallow import Schema, fields, INCLUDE, EXCLUDE

class BookSchema(Schema):
    id = fields.Int()
    title = fields.Str(required = True)
    author = fields.Str(required = True)

resp_get_json = {'author': 'Franklin', 'title': 'Crime and mystery story'}

book_schema = BookSchema()
book_obj = book_schema.load(resp_get_json)
print(book_obj)