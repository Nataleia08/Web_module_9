from mongoengine import Document
from mongoengine.fields import ListField, StringField, DateField, ReferenceField, BooleanField, IntField


class Authors(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()
class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors)
    quote = StringField()

class Contact(Document):
    fullname = StringField()
    email = StringField()
    send_email = BooleanField(default=False)
    send_sms = BooleanField(default=False)
    phone = StringField()
    type_chanel = IntField()
