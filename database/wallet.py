import typing
from datetime import datetime
from google.cloud import ndb
from database.mixins import AmountMixin
from config.exception_handlers import handle_store_errors
from database.setters import setters


class WalletValidator:
    def __init__(self):
        pass

    @staticmethod
    @handle_store_errors
    def wallet_exist(uid: str) -> typing.Union[bool, None]:
        wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
        return True if isinstance(wallet_instance, WalletModel) else False

    @staticmethod
    @handle_store_errors
    async def wallet_exist_async(uid: str) -> typing.Union[bool, None]:
        wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get_async().get_result()
        return True if isinstance(wallet_instance, WalletModel) else False

    # TODO complete validations for all Wallet Models
    # TODO be sure to integrate all models to the view


class WalletModel(ndb.Model):
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    available_funds: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=setters.set_funds)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True)
    paypal_address: str = ndb.StringProperty(validator=setters.set_paypal)

    def __str__(self) -> str:
        return "<Wallet {}{}{}{}".format(self.paypal_address, self.available_funds, self.time_created,
                                         self.last_transaction_time)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.paypal_address != other.paypal_address:
            return False
        return True

    def __len__(self) -> int:
        return len(self.uid)

    def __bool__(self) -> bool:
        return bool(self.uid)


class WalletTransactionsModel(ndb.Model):
    organization_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=setters.set_id)
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    transaction_type: str = ndb.StringProperty(validator=setters.set_transaction_types)
    transaction_date: str = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_datetime)

    def __str__(self) -> str:
        return "<Transactions {} {}".format(self.transaction_type, self.transaction_date)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_type != other.transaction_type:
            return False
        if self.transaction_date != other.transaction_date:
            return False
        return True

    def __len__(self) -> int:
        return len(self.uid) and len(self.transaction_id)

    def __bool__(self) -> bool:
        return bool(self.uid) or bool(self.transaction_id)


class WalletTransactionItemModel(ndb.Model):
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    item_id: str = ndb.StringProperty(validator=setters.set_id)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_verified: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

    def __str__(self) -> str:
        return "{}{}".format(self.amount, self.is_verified)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.item_id != other.item_id:
            return False
        if self.amount != other.amount:
            return False
        return True

    def __len__(self) -> int:
        return len(self.transaction_id)

    def __bool__(self) -> bool:
        # return True if self.transaction_id else False
        return bool(self.transaction_id)
