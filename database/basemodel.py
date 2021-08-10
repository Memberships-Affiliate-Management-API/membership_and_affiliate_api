***REMOVED***
    **ndb BaseModel **
        used as a superclass to define data models
***REMOVED***
from google.cloud import ndb


class BaseModel(ndb.Model):

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return int(self.__bool__())

    @property
    def urlsafe_key(self) -> bytes:
        return self.key.urlsafe()

    # Turns the class to dict and include instance key
    def to_dict(self) -> dict: return super().to_dict().update(key=self.urlsafe_key)

    @staticmethod
    def get_instance_by_key(key: bytes) -> ndb.Model:
        ***REMOVED***
            returns the model instance from a key in byte string format
        :param key:
        :return:
        ***REMOVED***
        return ndb.Key(urlsafe=key).get()
