***REMOVED***
    **Wallet Module**
    *Wallet Classes For Management of Clients / Organizations and Users Wallets"
***REMOVED***
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_repo__ = "https://github.com/freelancing-solutions/memberships-and-affiliate-api"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from datetime import datetime
from google.cloud import ndb
from config.currencies import currency_util
from database.mixins import AmountMixin
from config.exception_handlers import handle_store_errors
from database.setters import property_
from database.basemodel import BaseModel


class WalletValidator:
    ***REMOVED***
        **Class WalletValidator**
            Validates User Inputs when creating updating and making transactions on clients
            and organizational wallets

    ***REMOVED***

    def __init__(self):
        pass

    @staticmethod
    @handle_store_errors
    def wallet_exist(organization_id: str, uid: str) -> typing.Union[bool, None]:
        ***REMOVED***
            **wallet_exist**
                checks if a specific wallet exists

        :param 1. organization_id: the id of the organization the wallet belongs to
        :param 2. uid: the user id of the user the wallet belong to
        :return: boolean True / False representing if wallet exists or not
        ***REMOVED***

        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get()
        # returns true if wallet is found
        return bool(wallet_instance)

    @staticmethod
    @handle_store_errors
    async def wallet_exist_async(organization_id: str, uid: str) -> typing.Union[bool, None]:
        ***REMOVED***
            **wallet_exist_async**
                asynchronous version of wallet exists
        :param organization_id:
        :param uid:
        :return:
        ***REMOVED***
        wallet_instance: WalletModel = WalletModel.query(WalletModel.organization_id == organization_id,
                                                         WalletModel.uid == uid).get_async().get_result()

        # returns true if wallet exists
        return bool(wallet_instance)

    # TODO complete validations for all Wallet Models
    # TODO be sure to integrate all models to the view


class WalletModel(BaseModel):
    ***REMOVED***
        **WALLET Documentations:**

        **Wallet Class**
            1. Represents a wallet for clients and organizations
            2. validates data through setters defined on module setters

        **NOTE:**
            1. When a wallet belongs to an organization is_org_wallet will be true, else False.
            2. organization_id indicates the user organization or the organization the wallet belongs to depending
            on the value of is_org_wallet
            3. On a monthly basis reset monthly_withdrawal_allowance

        **Wallet Properties**
            1. organization_id : id of the organization for this wallet
            2. is_org_wallet : True if wallet belongs to an organization
            3. uid : id of the user who owns this wallet if is_org_wallet is false
            4. available_funds : Amount indicating available_funds in the wallet
            5. time_created: The time the wallet has been created
            6. last_transaction_time: the last time a transaction has been made in this wallet
            7. paypal_address : the paypal address attached to this wallet
            8. is_verified: Indicates if paypal_address has been verified
    ***REMOVED***
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    is_org_wallet: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True, required=True)
    available_funds: AmountMixin = ndb.StructuredProperty(AmountMixin, required=True)
    monthly_withdrawal_allowance: AmountMixin = ndb.StructuredProperty(AmountMixin)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)
    paypal_address: str = ndb.StringProperty(validator=property_.set_paypal)
    is_verified: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)

    def __str__(self) -> str:
        return "<Wallet {}{}{}{}".format(self.paypal_address, self.available_funds, self.time_created,
                                         self.last_transaction_time)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.paypal_address != other.paypal_address:
            return False
        return True

    def __bool__(self) -> bool:
        return bool(self.uid) and bool(self.organization_id)

    @property
    def can_withdraw(self) -> bool:
        ***REMOVED***
            **Property**
                True if withdrawals can be undertaken - this is dependent on amount availability and also
                if paypal address is present and also verified

            **Documentation**
                will check if available_funds meets the recommended minimum withdrawal amount if yes returns True

            :return: bool ->if True: there is enough funds on the wallet in order to create a withdrawal transaction
                    otherwise False
        ***REMOVED***
        minimum_withdrawal: int = currency_util.return_minimum_withdrawal_by_currency(
            currency_symbol=self.available_funds.currency)

        return minimum_withdrawal <= self.available_funds.amount_cents if self.paypal_address and self.is_verified else False

    @property
    def drawable_amount(self) -> AmountMixin:
        ***REMOVED***
            **Property**
                Amount that can be withdrawn right now

            **Documentation**
                1. If available funds is more than withdrawal limit return withdrawal limit lest return available_funds
                2. returns the maximum amount of money that can be withdrawn in one transaction

        :return: AmountMixin Representing the Maximum Amount of Money which can be withdrawn
        ***REMOVED***
        if not self.can_withdraw:
            # Returns zero as withdrawal limit, as the available funds are below the minimum withdrawal limit
            return AmountMixin(amount=0, currency=self.available_funds.currency)
        if self.monthly_withdrawal_allowance.currency != self.available_funds.currency:
            raise ValueError("Wallet is configured in-properly currencies do not match")
        # NOTE taking cents from AmountMixin
        avail_funds: int = self.available_funds.amount_cents
        allowance: int = self.monthly_withdrawal_allowance.amount_cents

        return self.monthly_withdrawal_allowance if avail_funds > allowance else self.available_funds


class WalletTransactionsModel(BaseModel):
    ***REMOVED***
        **Class WalletTransactionItemModel**
            a model to keep track of each transaction item and amount that belongs to the
            transaction mentioned in  **WalletTransactionsModel**

        **Class Properties**
            1. transaction_id: string -> transaction_id relates this record with the actual transaction taking place
            2. item_id: string -> item_id uniquely identifies this transaction item
            3. amount: AmountMixin -> amount of money in this transaction
            4. is_verified: bool -> true if transaction has been verified

        **NOTE**
            once a transaction has been verified amounts can change hands or transferred from
            actual accounts
    ***REMOVED***
    organization_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    uid: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    transaction_id: str = ndb.StringProperty(default=None, validator=property_.set_id, indexed=True)
    transaction_type: str = ndb.StringProperty(validator=property_.set_transaction_types)
    transaction_date: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=property_.set_datetime)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=property_.set_datetime)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_verified: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)
    is_settled: bool = ndb.BooleanProperty(default=False, validator=property_.set_bool)

    def __str__(self) -> str:
        return "{}{}".format(self.amount, self.is_verified)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.item_id != other.item_id:
            return False
        if self.amount != other.amount_cents:
            return False
        return True

    def __bool__(self) -> bool:
        # return True if self.transaction_id else False
        return bool(self.transaction_id) and bool(self.uid) and bool(self.organization_id)
