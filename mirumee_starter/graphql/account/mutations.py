import graphene
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..core.utils import staff_only, superuser_only

import re

from .types import UserType
from ...account.models import User


class UserCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)

    is_staff = graphene.Boolean(default=False)
    is_active = graphene.Boolean(default=True)


class StaffCreateInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)

    is_staff = graphene.Boolean(default=True)
    is_active = graphene.Boolean(default=True)


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserCreateInput(required=True)

    # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    @classmethod
    def clean_email(cls, email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not re.search(regex, email):
            raise ValidationError('The email is incorrect.')
        return email

    @classmethod
    def clean_password(cls, password):
        # Wymagania dotyczące hasła np. długość, jedna wielka litera, jeden znak specjalny, jedna liczba itp.
        return password

    @classmethod
    def clean_input(cls, input):
        input['email'] = cls.clean_email(input['email'])
        input['password'] = cls.clean_password(input['password'])
        return input

    @classmethod
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)

        password = cleaned_input.pop('password')

        user = User.objects.create(**cleaned_input)
        user.set_password(password)
        user.save()

        return UserCreate(user=user)


class StaffCreate(graphene.Mutation):
    staff = graphene.Field(UserType)

    class Arguments:
        input = StaffCreateInput(required=True)

    # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    @classmethod
    def clean_email(cls, email):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not re.search(regex, email):
            raise ValidationError('The email is incorrect.')
        return email

    @classmethod
    def clean_password(cls, password):
        # Wymagania dotyczące hasła np. długość, jedna wielka litera, jeden znak specjalny, jedna liczba itp.
        return password

    @classmethod
    def clean_input(cls, input):
        input['email'] = cls.clean_email(input['email'])
        input['password'] = cls.clean_password(input['password'])
        return input

    @classmethod
    @superuser_only
    def mutate(cls, root, info, input):
        cleaned_input = cls.clean_input(input)

        email = cleaned_input.pop('email')

        try:
            staff = User.objects.get(email=email)
        except ObjectDoesNotExist:
            staff = User.objects.create(
                email=email,
                **cleaned_input)

            return StaffCreate(staff=staff)

        staff.is_staff = True
        staff.save()

        return StaffCreate(staff=staff)
