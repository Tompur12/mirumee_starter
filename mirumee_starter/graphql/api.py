import graphene

from ..graphql.product.schema import ProductQueries, ProductMutations
from ..graphql.chceckout.schema import CheckoutQueries, CheckoutMutations
from ..graphql.account.authenticate import AuthenticateMutation
from ..graphql.account.schema import UserQueries, UserMutations


class Query(ProductQueries, CheckoutQueries, UserQueries):
    pass


class Mutations(ProductMutations, CheckoutMutations, AuthenticateMutation, UserMutations):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
