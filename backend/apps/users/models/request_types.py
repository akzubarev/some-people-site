from dataclasses import dataclass

from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from mixins.events import DataType


@dataclass
class ActionRequestType(DataType):
    pass


@dataclass
class TransactionRequest(ActionRequestType):
    type: str = None
    amount: int = None

    @cached_property
    def title(self):
        return _('Transaction request')


@dataclass
class OldEmailChangeRequest(ActionRequestType):
    email: str = None

    @cached_property
    def title(self):
        return _('Change email old')


@dataclass
class NewEmailChangeRequest(ActionRequestType):
    email: str = None

    @cached_property
    def title(self):
        return _('Change email new')
