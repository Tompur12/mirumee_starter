from graphql_jwt.exceptions import PermissionDenied
import graphql.type
from functools import wraps


def staff_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        for arg in args:
            if type(arg) is graphql.type.GraphQLResolveInfo:
                info = arg
                break
        if info.context.user.is_staff:
            response = function(*args, **kwargs)
        else:
            raise PermissionDenied
        return response
    return wrapper


def superuser_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        for arg in args:
            if type(arg) is graphql.type.GraphQLResolveInfo:
                info = arg
                break
        if info.context.user.is_superuser:
            response = function(*args, **kwargs)
        else:
            raise PermissionDenied
        return response
    return wrapper
