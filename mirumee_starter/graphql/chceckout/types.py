import graphene
from django.db.models import F
from graphene_django import DjangoObjectType

from ...checkout.models import Checkout, CheckoutLine


class CheckoutLineType(DjangoObjectType):
    total_price_of_checkout_line = graphene.Decimal(description='Total price of checkout line.')

    class Meta:
        model = CheckoutLine
        fields = '__all__'

    def resolve_total_price_of_checkout_line(self, _info):
        total_price = self.variant.price * self.quantity

        return total_price


class CheckoutType(DjangoObjectType):
    total_checkout_price = graphene.Decimal(description='Total price of checkout.')

    class Meta:
        model = Checkout
        fields = '__all__'

    def resolve_total_checkout_price(self, _info):

        total_price = self.lines.annotate(
            total_price=F('quantity') * F('variant__price')).values_list('total_price', flat=True)
        return sum(total_price)
