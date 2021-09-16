import graphene

from ...checkout.models import Checkout, CheckoutLine
from .mutations import CheckoutCreate, CheckoutLineCreate
from .types import CheckoutLineType, CheckoutType
from ..core.utils import staff_only


class CheckoutQueries(graphene.ObjectType):
    checkout = graphene.Field(
        CheckoutType,
        id=graphene.Argument(graphene.ID, description="ID of checkout."),
    )
    checkouts = graphene.List(CheckoutType)
    checkout_line = graphene.Field(
        CheckoutType,
        id=graphene.Argument(graphene.ID, description="Id of checkout line."),
    )
    checkout_lines = graphene.List(CheckoutLineType)

    def resolve_checkout(self, info, id):
        checkout = Checkout.objects.filter(id=id).first()
        return checkout

    @staff_only
    def resolve_checkouts(self, info):
        checkouts = Checkout.objects.all()
        return checkouts


class CheckoutMutations(graphene.ObjectType):
    checkout_create = CheckoutCreate.Field()
    checkout_line_create = CheckoutLineCreate.Field()
