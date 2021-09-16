import graphene
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .types import CheckoutType, CheckoutLineType
from ...checkout.models import Checkout, CheckoutLine
from ...product.models import ProductVariant


class CheckoutLineCreateInput(graphene.InputObjectType):
    quantity = graphene.Int(required=True, description="The number of items purchased.")
    variant_id = graphene.ID(required=True, description="ID of the product variant.")


class CheckoutCreateInput(graphene.InputObjectType):
    user_email = graphene.String()
    lines = graphene.List(CheckoutLineCreateInput, required=True)


class CheckoutCreate(graphene.Mutation):
    checkout = graphene.Field(CheckoutType)

    class Arguments:
        input = CheckoutCreateInput(required=True)
        user_id = graphene.ID(required=False)

    @classmethod
    def clean_email(cls, email):
        return email

    @classmethod
    def clean_lines(cls, lines):
        for line in lines:
            if line['quantity'] <= 0:
                raise ValidationError('The quantity cannot be negative or equal to 0.')
            if not ProductVariant.objects.filter(id=line['variant_id']).exists():
                raise ValidationError('There is no such product variant.')
        return lines

    @classmethod
    def clean_input(cls, input):
        input['user_email'] = cls.clean_email(input['user_email'])
        input['lines'] = cls.clean_lines(input['lines'])
        return input

    @classmethod
    def create_checkout_lines(cls, lines, checkout_id):
        checkout_lines = []
        for line in lines:
            try:
                checkout_line = CheckoutLine.objects.get(checkout_id=checkout_id, variant_id=line['variant_id'])
                checkout_line.quantity += line['quantity']
                checkout_line.save()
            except ObjectDoesNotExist:
                checkout_lines.append(CheckoutLine(checkout_id=checkout_id, **line))

        return checkout_lines

    @classmethod
    def mutate(cls, root, info, input, user_id):
        cleaned_input = cls.clean_input(input)

        email = cleaned_input.pop("user_email")

        if info.context.user.is_authenticated:

            try:
                checkout = Checkout.objects.get(user_email=info.context.user.email)
            except ObjectDoesNotExist:
                lines = input.pop('lines')
                checkout = Checkout.objects.create(user_id=info.context.user.id, user_email=info.context.user.email)

                checkout.lines.bulk_create(cls.create_checkout_lines(lines, checkout.id))

                return CheckoutCreate(checkout=checkout)

            lines = cleaned_input.pop('lines')

            checkout.lines.bulk_create(cls.create_checkout_lines(lines, checkout.id))
            return CheckoutCreate(checkout=checkout)

        else:
            try:
                checkout = Checkout.objects.get(user_email=email)
            except ObjectDoesNotExist:
                lines = cleaned_input.pop('lines')
                checkout = Checkout.objects.create(user_id=user_id, user_email=email)

                checkout.lines.bulk_create(cls.create_checkout_lines(lines, checkout.id))

                return CheckoutCreate(checkout=checkout)

            lines = cleaned_input.pop('lines')

            checkout.lines.bulk_create(checkout.lines.bulk_create(cls.create_checkout_lines(lines, checkout.id)))
            return CheckoutCreate(checkout=checkout)


class CheckoutLineCreate(graphene.Mutation):
    checkout_line = graphene.Field(CheckoutLineType)

    class Arguments:
        input = CheckoutLineCreateInput(required=True)
        checkout_id = graphene.ID(required=True)

    @classmethod
    def clean_checkout_id(cls, checkout_id):
        if not Checkout.objects.filter(id=checkout_id).exists():
            raise ValidationError('There is no such checkout.')
        return checkout_id

    @classmethod
    def clean_input(cls, input):
        if input['quantity'] <= 0:
            raise ValidationError('The quantity cannot be negative or equal to 0.')
        if not ProductVariant.objects.filter(id=int(input['variant_id'])).exists():
            raise ValidationError('There is no such product variant.')
        return input

    @classmethod
    def mutate(cls, root, info, input, checkout_id):
        cleaned_input = cls.clean_input(input)
        checkout_id = cls.clean_checkout_id(int(checkout_id))
        variant_id = cleaned_input.pop('variant_id')
        input_quantity = cleaned_input.pop('quantity')

        try:
            checkout_line = CheckoutLine.objects.get(checkout_id=checkout_id, variant=variant_id)
        except ObjectDoesNotExist:
            checkout_line = CheckoutLine.objects.create(
                checkout_id=checkout_id,
                variant_id=variant_id,
                quantity=input_quantity)

            return CheckoutLineCreate(checkout_line=checkout_line)

        quantity = checkout_line.quantity + input_quantity

        checkout_line.quantity = quantity
        checkout_line.save()

        return CheckoutLineCreate(checkout_line=checkout_line)
