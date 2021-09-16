import graphene
from django.core.exceptions import ValidationError

from .types import ProductType, ProductVariantType
from ...product.models import Product, ProductVariant
from ..core.utils import staff_only


class ProductCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    descrpiton = graphene.String(required=True)
    quantity = graphene.Int()


class ProductCreate(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        input = ProductCreateInput(required=True)

    @classmethod
    def clean_price(cls, price):
        if price <= 0:
            raise ValidationError('The price cannot be negative.')
        return price

    @classmethod
    def clean_quantity(cls, quantity):
        if quantity < 0:
            raise ValidationError('The quantity cannot be negative.')
        return quantity

    @classmethod
    def clean_input(cls, input):
        input['price'] = cls.clean_price(input['price'])
        input['quantity'] = cls.clean_quantity(input['quantity'])
        return input

    @classmethod
    @staff_only
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)

        product = Product.objects.create(**cleaned_input)

        return ProductCreate(product=product)


class ProductVariantCreateInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    sku = graphene.String(required=True)
    price = graphene.Decimal()


class ProductVariantCreate(graphene.Mutation):
    product_variant = graphene.Field(ProductVariantType)

    class Arguments:
        input = ProductVariantCreateInput(required=True)
        product_id = graphene.ID(required=True)

    @classmethod
    def clean_price(cls, price):
        if price <= 0:
            raise ValidationError('The price cannot be negative.')
        return price

    @classmethod
    def clean_sku(cls, sku):
        if ProductVariant.objects.filter(sku=sku).exists():
            raise ValidationError('This SKU already exist.')
        return sku

    @classmethod
    def clean_product_id(cls, product_id):
        if Product.objects.filter(id=product_id).exists():
            return product_id
        raise ValidationError('The product you want to make a variant does not exist.')

    @classmethod
    def clean_input(cls, input):
        price = input.get('price')
        if price:
            input['price'] = cls.clean_price(price)
        input['sku'] = cls.clean_sku(input['sku'])
        return input

    @classmethod
    @staff_only
    def mutate(cls, root, info, input, product_id):
        cleaned_input = cls.clean_input(input)
        product_id = cls.clean_product_id(product_id)

        product_variant = ProductVariant.objects.create(product_id=product_id, **cleaned_input)

        return ProductVariantCreate(product_variant=product_variant)
