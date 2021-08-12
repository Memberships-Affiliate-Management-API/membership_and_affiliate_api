***REMOVED***
    **ndb BaseModel **
        used as a superclass to define data models
***REMOVED***
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
                equivalent to __str__
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
    def id(self):
        ***REMOVED***int: The index ID.***REMOVED***
        return self.key.id() if self.key else None

    @property
    def urlsafe_key(self) -> bytes:
        ***REMOVED***
            **urlsafe_key**
                byte representation of key in order to enable
                sending the key over requests calls
        :return: bytes representing datastore key
        ***REMOVED***
        return self.key.urlsafe()

    # Turns the class to dict and include instance key
    def to_dict(self, include=all, exclude=None) -> dict:
        ***REMOVED***
            **to_dict**
                based on the super dict method of ndb.Model
                return a customized dict with the difference that every result
                includes ndb.Key
        :return: dict rep of instance
        ***REMOVED***
        return super().to_dict(include=include, exclude=exclude).update(key=self.urlsafe_key)

    @staticmethod
    def get_instance_by_key(key: bytes) -> ndb.Model:
        ***REMOVED***
            returns the model instance from a key in byte string format
        :param key: byte ndb. Key
        :return: ndb instance fetched by key
        ***REMOVED***
        return ndb.Key(urlsafe=key).get()
