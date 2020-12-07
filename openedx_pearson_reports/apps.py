"""
File configuration for openedx-proversity-reports.
"""
from django.apps import AppConfig


class OpenEdxProversityReportsConfig(AppConfig):
    """
    Plugin app configuration for openedx-proversity-reports
    """
    name = 'openedx_proversity_reports'
    verbose_name = "Open edX Proversity additional reports plugin."

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'production': {'relative_path': 'settings.production'},
            },
        },
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'proversity-reports',
                'regex': r'^proversity-reports/',
                'relative_path': 'urls',
            },
        },
    }

    def ready(self):
        """
        The line below allows tasks defined in this app to be included by celery workers.
        https://docs.djangoproject.com/en/2.2/ref/applications/#django.apps.AppConfig.ready

        Due to a presumed circular import, the tasks are imported individually instead of importing
        all the definitions in .tasks file.
        """
        from .tasks import (
            enrollment_per_site_report_task,
        )
