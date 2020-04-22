from django.urls import path, include
from django.views import i18n
from rest_framework.routers import DefaultRouter

from apps.api.views.thesis import ThesisViewSet

router = DefaultRouter()
router.register(r'thesis', ThesisViewSet)

app_name = 'api'
urlpatterns = [
    path('v1/', include((router.urls, 'v1'))),

    # TODO: add vue-i18n with data from this view
    path('i18n/', i18n.JSONCatalog.as_view(domain='django')),
]