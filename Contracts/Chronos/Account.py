#pylint: skip-file
from Chronos.Core import Aggregate, Event, ChronosIndex
from Account_pb2 import Account, CreateEvent, DepositEvent, WithdrawEvent

class AccountIndex(ChronosIndex):
    attributes = ('owner',)

class Account(Aggregate):
    Proto = Account
    Index = AccountIndex


    def IsValid(self):
        return True

class CreateEvent(Event):
    Aggregate = Account
    Proto = CreateEvent

    def RaiseFor(self, aggregate):
        aggregate.owner = self.owner
        aggregate.balance = self.initialAmount

class DepositEvent(Event):
    Aggregate = Account
    Proto = DepositEvent

    def RaiseFor(self, aggregate):
        aggregate.balance += self.amount

class WithdrawEvent(Event):
    Aggregate = Account
    Proto = WithdrawEvent

    def RaiseFor(self, aggregate):
        aggregate.balance -= self.amount
