"""
Api URLs.
"""
from django.conf.urls import include, url


app_name = 'api'
urlpatterns = [  # pylint: disable=invalid-name
    url(r'v0/', include(('openedx_proversity_reports.api.v0.urls', app_name), namespace='v0')),
    url(r'v1/', include(('openedx_proversity_reports.api.v1.urls', app_name), namespace='v1')),
]
