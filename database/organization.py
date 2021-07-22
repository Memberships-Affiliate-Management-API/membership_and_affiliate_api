from google.cloud import ndb
from database.mixins import AmountMixin


class Organization(ndb.Model):
    owner_uid: str = ndb.StringProperty()
    organization_id: str = ndb.StringProperty()
    organization_name: str = ndb.StringProperty()
    total_affiliates: int = ndb.IntegerProperty()
    total_paid: AmountMixin = ndb.StructuredProperty(AmountMixin)


class OrgAccounts(ndb.Model):
    ***REMOVED***
        include details of the main organization payments accounts here
    ***REMOVED***
    organization_id: str = ndb.StringProperty()
    paypal_email: str = ndb.StringProperty()


class PaymentResults(ndb.Model):
    ***REMOVED***
        for every payment which is approved by admin, retain the result of the payment here
    ***REMOVED***
    organization_id: str = ndb.StringProperty()
    transaction_id: str = ndb.StringProperty()
    payment_result: str = ndb.StringProperty()



