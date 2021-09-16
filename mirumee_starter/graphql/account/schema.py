import graphene

from ...account.models import User
from .mutations import UserCreate, StaffCreate
from .types import UserType
from ..core.utils import staff_only


class UserQueries(graphene.ObjectType):
    user = graphene.Field(
        UserType,
        email=graphene.Argument(graphene.String, description='Email of user.'),
    )

    users = graphene.List(UserType)

    def resolve_user(self, info, email):
        user = User.objects.filter(email=email).first()
        return user

    @staff_only
    def resolve_users(self, info):
        users = User.objects.all()
        return users


class UserMutations(graphene.ObjectType):
    user_create = UserCreate.Field()
    staff_create = StaffCreate.Field()
