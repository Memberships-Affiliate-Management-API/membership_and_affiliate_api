***REMOVED***
    Services Module works together with memberships module
    for example for a music streaming service a plan will be created
    in MembershipsPlans in the Memberships Module and also
    on PayPal, when a user subscribes to a plan the subscription
    will be created both on Memberships Module and also on PayPal
    so that the subscription amount can be taken off the user paypal_address

***REMOVED***
from google.cloud import ndb
from database.setters import setters


class Services(ndb.Model):
    ***REMOVED***
        The Services Module, will capture the service data
        the information here will be similar to the information
        on paypal services or products for plans...
    ***REMOVED***
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    service_id: str = ndb.StringProperty(validator=setters.set_id)
    name: str = ndb.StringProperty(validator=setters.set_string)
    description: str = ndb.StringProperty(validator=setters.set_string)

