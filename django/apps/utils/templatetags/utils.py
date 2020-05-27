import re
from audioop import reverse

from django import template
from django.conf import settings
from django.db.models import Choices, Model
from django.http import HttpRequest
from django.urls import reverse
from django.utils import translation
from django.utils.html import json_script

from apps.accounts.serializers import UserSerializer

register = template.Library()


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter
def get_choices_display(value, choices: Choices):
    return choices(value).label


@register.simple_tag
def get_verbose_field_name(instance: Model, field_name: str):
    return instance._meta.get_field(field_name).verbose_name


@register.simple_tag
def absolute_url(view_name, *args, **kwargs):
    return f'{settings.PUBLIC_HOST.rstrip("/")}{reverse(view_name, args=args, kwargs=kwargs)}'


@register.simple_tag(takes_context=True)
def page_context(context, element_id, _re_language=re.compile(r'[_-]'), *args, **kwargs):
    request: HttpRequest = context['request']

    user = request.user
    return json_script(dict(
        locale=_re_language.split(translation.get_language())[0],
        user=UserSerializer(instance=user).data,
        groups=tuple(user.groups.values_list('name', flat=True)),
        djangoAdminUrl=reverse('admin:index') if user.is_staff else '',
        languages=[(k, translation.gettext(v)) for k, v in settings.LANGUAGES],
        version=settings.VERSION,
    ), element_id)