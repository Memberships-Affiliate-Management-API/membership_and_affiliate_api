***REMOVED***
    **Types***
    Type Definitions for All DataClasses
***REMOVED***


from enum import Enum, Flag, auto


class TransactionTypes(Enum):
    ***REMOVED***Transaction Types***REMOVED***
    Withdrawal = 'withdrawal'
    Deposit = 'deposit'
    Refund = 'refund'


class PaymentStatusTypes(Enum):
    ***REMOVED***Payment statuses***REMOVED***
    Paid = 'paid'
    UnPaid = 'unpaid'
    PaymentFailed = 'payment-failed'

