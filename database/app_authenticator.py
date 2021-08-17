***REMOVED***
    **App Authenticator database**

***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from google.cloud import ndb


class AppsDetails(ndb.Model):
    ***REMOVED***
        **Class AppsDetails**

    ***REMOVED***
    domain: str = ndb.StringProperty()
    secret_key: str = ndb.StringProperty()
    auth_token: str = ndb.StringProperty()
