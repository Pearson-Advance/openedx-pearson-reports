"""
Django settings for openedx_pearson_reports project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = []


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # pylint: disable=line-too-long
    settings.OPR_BLOCK_STRUCTURE_LIBRARY = 'openedx_pearson_reports.edxapp_wrapper.backends.block_structure_i_v1'
    settings.OPR_CERTIFICATES_MODELS = 'openedx_pearson_reports.edxapp_wrapper.backends.certificates_models_i_v1'
    settings.OPR_COMPLETION_MODELS = 'openedx_pearson_reports.edxapp_wrapper.backends.completion_models_j_v1'
    settings.OPR_COURSE_BLOCKS = 'openedx_pearson_reports.edxapp_wrapper.backends.course_blocks_i_v1'
    settings.OPR_COURSE_COHORT = 'openedx_pearson_reports.edxapp_wrapper.backends.course_cohort_i_v1'
    settings.OPR_COURSE_GRADE_LIBRARY = 'openedx_pearson_reports.edxapp_wrapper.backends.course_grade_i_v1'
    settings.OPR_COURSE_TEAMS = 'openedx_pearson_reports.edxapp_wrapper.backends.course_teams_i_v1'
    settings.OPR_COURSEWARE_LIBRARY = 'openedx_pearson_reports.edxapp_wrapper.backends.courseware_i_v1'
    settings.OPR_EDX_REST_FRAMEWORK_EXTENSIONS = 'openedx_pearson_reports.edxapp_wrapper.backends.edx_rest_framework_extensions_j_v1'
    settings.OPR_MODULESTORE = 'openedx_pearson_reports.edxapp_wrapper.backends.modulestore_i_v1'
    settings.OPR_STUDENT_ACCOUNT_LIBRARY = 'openedx_pearson_reports.edxapp_wrapper.backends.student_account_g_v1'
    settings.OPR_STUDENT_LIBRARY = 'openedx_pearson_reports.edxapp_wrapper.backends.student_i_v1'
    settings.OPR_COURSE_API = 'openedx_pearson_reports.edxapp_wrapper.backends.course_api_j_v1'
    settings.OPR_GOOGLE_ANALYTICS_CREDENTIALS = {}
    settings.OPR_GOOGLE_ANALYTICS_VIEW_ID = ''
    settings.OPR_COURSEWARE_LIBRARY = 'openedx_pearson_reports.edxapp_wrapper.backends.courseware_i_v1'
    settings.OPR_SUPPORTED_TASKS = [
        'generate_last_page-accessed_report',
        'generate_time_spent_report',
        'generate_learning_tracker_report',
        'generate_enrollment_report',
        'generate_activity_completion_report',
        'generate_time_spent_per_user_report',
        'generate_last_login_report',
    ]
    settings.OPR_TIME_BETWEEN_SESSIONS = 5  # This value is in minutes.
    settings.OPR_COURSE_DETAILS = 'openedx_pearson_reports.edxapp_wrapper.backends.course_details_g_v1'
    settings.OPR_GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = {}
    settings.OPR_GOOGLE_CLOUD_PROJECT_ID = ''
    settings.OPR_GOOGLE_BIGQUERY_MAX_PROCESS_BYTES = 10485760  # 10MB
    settings.OPR_GOOGLE_BIGQUERY_MAX_NUMBER_RESULTS_PER_QUERY = 1000
    settings.OPR_GOOGLE_BIGQUERY_USE_CACHE = True
    settings.OPR_GOOGLE_BIGQUERY_TIME_ON_ASSET_DAILY_COLUMN_NAME = 'time_umid30'
    settings.OPR_SUPPORTED_REPORTS_BACKENDS = {
        'generate_enrollment_per_site_report': {
            'backend': 'openedx_pearson_reports.reports.backend.enrollment_per_site_report:EnrollmentReportPerSiteBackend',
            'max_results_per_page': 10,
        },
        'generate_completion_report': {
            'backend': 'openedx_pearson_reports.reports.completion_report:CompletionReportBackend',
            'max_results_per_page': 5,
        },
    }
    settings.OPR_DEFAULT_PAGE_RESULTS_LIMIT = 10
    settings.OPR_COURSE_CONTENT = 'openedx_pearson_reports.edxapp_wrapper.backends.course_content_i_v1'
    settings.OPR_OPENEDX_AUTHENTICATION = 'openedx_pearson_reports.edxapp_wrapper.backends.openedx_authentication_j_v1'
