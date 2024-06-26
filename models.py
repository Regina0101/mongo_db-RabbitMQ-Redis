from connect import connect
from mongoengine import Document, StringField, ReferenceField, ListField

class Author(Document):
    fullname = StringField(required=True)
    born_date =  StringField()
    born_location = StringField(max_length=50)
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Author, required=True)
    quote = StringField()

