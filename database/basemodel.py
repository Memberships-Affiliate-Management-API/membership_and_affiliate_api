"""
    **ndb BaseModel **
        used as a superclass to define data models
"""

__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"
__licence__ = "MIT"

from typing import Optional, List
from google.cloud import ndb
from config.use_context import use_context


class BaseModel(ndb.Model):
    """
        **BaseModel**
            defines common d_under methods, properties and methods
            used to define all other Data Models
    """
    def __bool__(self) -> bool:
        """bool protocol"""
        ...

    def __repr__(self) -> str:
        """
            **__repr__**
                equivalent to __str__, but has to be unique for each instance
        :return: string rep of instance
        """
        return f"{type(self).__name__} (id={self.id} state={self.__str__()})"

    def __len__(self) -> int:
        """
            **__len__**
                defined to be equivalent to __bool__
        :return: int either 0 or 1 representing if instance is present or not
        """
        return int(self.__bool__())

    @ndb.model.ComputedProperty
    def id(self) -> Optional[str]:
        """
            **id**
            int: The index ID.
            return: key: str
        """
        return self.key.id() if isinstance(self.key, ndb.Key) else None

    @property
    def urlsafe_key(self) -> Optional[bytes]:
        """
            **urlsafe_key**
                byte representation of key in order to enable
                sending the key over requests calls

        :return: bytes representing datastore key
        """
        return self.key.urlsafe() if isinstance(self.key, ndb.Key) else None

    # Turns the class to dict and include instance key
    def to_dict(self, include: Optional[List[str]] = None, exclude:  Optional[List[str]] = None) -> dict:
        """
            **to_dict method**
                returns a full dict representing user except password property

        :param include: all
        :param exclude: password
        :return: dict -> all user properties excluding password
        """
        return super().to_dict(include=[prop._code_name for prop in self._properties.values()], exclude=exclude)

    @staticmethod
    @use_context
    def get_instance_by_key(key: bytes) -> ndb.Model:
        """
            **get_instance_by_key**
                returns the model instance from a key in byte string format

        :param key: byte ndb. Key
        :return: ndb instance fetched by key
        """
        return ndb.Key(urlsafe=key).get()

    def property_names_list(self) -> List[str]:
        """
        **property_names_list**
            returns a list of property names

        :return: List[str]
        """
        return [prop._code_name for prop in self._properties.values()]
