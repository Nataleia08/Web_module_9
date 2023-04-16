from MongoDB.models import Authors, Quotes
import json
import connect_bd
from mongoengine.errors import OperationError

with open("authors.json", "r") as fh:
    list_a = json.load(fh)
for a in list_a:
    try:
        na = Authors(fullname= a["fullname"], born_date = a["born_date"], born_location = a["born_location"], description = a["description"])
        na.save()
    except OperationError as err:
        print(err)

with open("quotes.json", "r") as fh:
    list_q = json.load(fh)
for q in list_q:
    try:
        author_ob = Authors.objects(fullname=q["author"])
        nq = Quotes(tags=q["tags"], author=author_ob[0], quote=q["quote"])
        nq.save()
    except OperationError as err:
        print(err)
