"""
    **Types***
    Type Definitions for All DataClasses
"""


from enum import Enum, Flag, auto


class TransactionTypes(Enum):
    """Transaction Types"""
    Withdrawal = 'withdrawal'
    Deposit = 'deposit'
    Refund = 'refund'


class PaymentStatusTypes(Enum):
    """Payment statuses"""
    Paid = 'paid'
    UnPaid = 'unpaid'
    PaymentFailed = 'payment-failed'

