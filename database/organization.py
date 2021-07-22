from google.cloud import ndb
from database.mixins import AmountMixin


class Organization(ndb.Model):
    owner_uid: str = ndb.StringProperty()
    organization_id: str = ndb.StringProperty()
    organization_name: str = ndb.StringProperty()
    total_affiliates: int = ndb.IntegerProperty()
    total_paid: AmountMixin = ndb.StructuredProperty(AmountMixin)

