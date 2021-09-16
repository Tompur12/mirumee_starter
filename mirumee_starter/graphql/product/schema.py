import graphene

from .types import ProductType, ProductVariantType
from ...product.models import Product, ProductVariant
from .mutations import ProductCreate, ProductVariantCreate


class ProductQueries(graphene.ObjectType):
    product = graphene.Field(ProductType, id=graphene.Argument(graphene.ID, description="ID of product."))

    products = graphene.List(ProductType)

    product_variant = graphene.Field(
        ProductVariantType, id=graphene.Argument(graphene.ID, description="ID of product variant.")
    )

    product_variants = graphene.List(ProductVariantType)

    def resolve_product(self, _info, id):
        product = Product.objects.filter(id=id).first()
        return product

    def resolve_products(self, _info):
        products = Product.objects.all()
        return products

    def resolve_product_variant(self, _info, id):
        product_variant = ProductVariant.objects.filter(id=id).first()
        return product_variant

    def resolve_product_variants(self, _info):
        product_variants = ProductVariant.objects.all()
        return product_variants


class ProductMutations(graphene.ObjectType):
    product_create = ProductCreate.Field()
    product_variant_create = ProductVariantCreate.Field()
