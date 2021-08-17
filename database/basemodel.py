***REMOVED***
    **ndb BaseModel **
        used as a superclass to define data models
***REMOVED***
__author__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

from typing import Optional

from google.cloud import ndb


class BaseModel(ndb.Model):
    ***REMOVED***
        **BaseModel**
            defines common d_under methods, properties and methods
            used to define all other Data Models
    ***REMOVED***
    def __repr__(self) -> str:
        ***REMOVED***
            **__repr__**
                equivalent to __str__, but has to be unique for each instance
        :return: string rep of instance
        ***REMOVED***
        return "{} (id={} state={})".format(type(self).__name__, self.id, self.__str__())

    def __len__(self) -> int:
        ***REMOVED***
            **__len__**
                defined to be equivalent to __bool__
        :return: int either 0 or 1 representing if instance is present or not
        ***REMOVED***
        return int(self.__bool__())

    @property
    def id(self) -> Optional[str]:
        ***REMOVED***int: The index ID.***REMOVED***
        return self.key.id() if isinstance(self.key, ndb.Key) else None

    @property
    def urlsafe_key(self) -> Optional[bytes]:
        ***REMOVED***
            **urlsafe_key**
                byte representation of key in order to enable
                sending the key over requests calls
        :return: bytes representing datastore key
        ***REMOVED***
        return self.key.urlsafe() if isinstance(self.key, ndb.Key) else None

    # Turns the class to dict and include instance key
    def to_dict(self, include=all, exclude=None) -> dict:
        ***REMOVED***
            **to_dict**
                based on the super dict method of ndb.Model
                return a customized dict with the difference that every result
                includes ndb.Key
        :return: dict rep of instance
        ***REMOVED***
        return super().to_dict(include=[include], exclude=[exclude]).update(key=self.urlsafe_key)

    @staticmethod
    def get_instance_by_key(key: bytes) -> ndb.Model:
        ***REMOVED***
            returns the model instance from a key in byte string format
        :param key: byte ndb. Key
        :return: ndb instance fetched by key
        ***REMOVED***
        return ndb.Key(urlsafe=key).get()
