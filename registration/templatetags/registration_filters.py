from django import template

from registration.models import User
from registration.definition import Privilege, Identity

register = template.Library()


@register.filter(name='has_permission')
def has_permission(user: User, required_privilege: Privilege):
    return user.has_permission(Privilege[required_privilege])


@register.filter(name='readableIdentity')
def readableIdentity(value):
    for identity in Identity.__members__.values():
        if value == identity.value[0]:
            return identity.value[1]