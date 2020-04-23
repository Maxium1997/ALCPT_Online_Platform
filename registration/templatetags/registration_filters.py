from django import template

from registration.models import User
from registration.definition import Privilege, Identity, Gender

register = template.Library()


@register.filter(name='has_permission')
def has_permission(user: User, required_privilege: Privilege):
    return user.has_permission(Privilege[required_privilege])


@register.filter(name='readableIdentity')
def readableIdentity(value):
    for identity in Identity.__members__.values():
        if value == identity.value[0]:
            return identity.value[1]


@register.filter(name='readableGender')
def readableGender(value):
    for gender in Gender.__members__.values():
        if value == gender.value[0]:
            return gender.value[1]
