from django import template

from registration.models import User
from registration.definition import Privilege

register = template.Library()


@register.filter(name='has_permission')
def has_permission(user: User, required_privilege: Privilege):
    return user.has_permission(Privilege[required_privilege])
