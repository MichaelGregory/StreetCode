"""
    StreetCodes - appliction models/REST interface.

    Note that all models will inherit a default name (StringProperty).
"""
from google.appengine.ext import db

import settings
import rest.models
from rest.models import RESTModel, Timestamped
import rest.counter as counter


def init():
    rest.models.add_models({
            'user': User,
            'sponsor': Sponsor,
            'client': Client,
            'donor': Donor,
            'transaction': Transaction,
            'scan': Scan,
            })


class Sponsor(RESTModel, Timestamped):
    url = db.StringProperty()
    address = db.TextProperty()
    phone = db.StringProperty()


class User(RESTModel, Timestamped):
    user = db.UserProperty()
    isAdmin = db.BooleanProperty()
    sponsor = db.ReferenceProperty(Sponsor)


class Client(RESTModel, Timestamped):
    fullName = db.StringProperty()
    shortCode = db.StringProperty()
    story = db.TextProperty()
    storyHTML = db.TextProperty()
    sponsor = db.ReferenceProperty(Sponsor)
    imageURL = db.StringProperty()

    form_order = ('name', 'fullName',
                  'shortCode',
                  'story', 'sponsor', 'imageURL',
                  'QRCode("http://streetcode.me/" + item.shortCode)'
                  )
    computed = ('item.storyHTML = markdown(item.story);',)


class Donor(RESTModel, Timestamped):
    address = db.TextProperty()
    phone = db.StringProperty()

    form_order = ('name', 'address', 'phone')


class Transaction(RESTModel, Timestamped):
    """
    Simple double-entry accounting.  Account names are in the format:

        'type_id/type_id'

    for example:
        'stripe'
        'sponsor_34/client_2'

    type is one of 'donation', 'fullfillment', ...
    """
    donor = db.ReferenceProperty(Donor)
    client = db.ReferenceProperty(Client)
    method = db.TextProperty()
    amount = db.FloatProperty()
    note = db.TextProperty()
    fullfilled = db.BooleanProperty(default=False)

    form_order = ('name', 'fromAccount', 'toAccount', 'amount', 'confirm')


class Scan(RESTModel, Timestamped):
    client = db.ReferenceProperty(Sponsor)
    donor = db.ReferenceProperty(Donor)
    ledger = db.ReferenceProperty(Transaction)

    form_order = ('name', 'client', 'donor', 'ledger')
