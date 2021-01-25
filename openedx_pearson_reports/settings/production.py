"""
Production settings for openedx_pearson_reports project.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OPR_BLOCK_STRUCTURE_LIBRARY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_BLOCK_STRUCTURE_LIBRARY',
        settings.OPR_BLOCK_STRUCTURE_LIBRARY
    )

    settings.OPR_CERTIFICATES_MODELS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_CERTIFICATES_MODELS',
        settings.OPR_CERTIFICATES_MODELS
    )

    settings.OPR_COMPLETION_MODELS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COMPLETION_MODELS',
        settings.OPR_COMPLETION_MODELS
    )

    settings.OPR_COURSE_BLOCKS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_BLOCKS',
        settings.OPR_COURSE_BLOCKS
    )

    settings.OPR_COURSE_COHORT = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_COHORT',
        settings.OPR_COURSE_COHORT
    )

    settings.OPR_COURSE_GRADE_LIBRARY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_GRADE_LIBRARY',
        settings.OPR_COURSE_GRADE_LIBRARY
    )

    settings.OPR_COURSE_TEAMS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_TEAMS',
        settings.OPR_COURSE_TEAMS
    )

    settings.OPR_COURSEWARE_LIBRARY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSEWARE_LIBRARY',
        settings.OPR_COURSEWARE_LIBRARY
    )

    settings.OPR_EDX_REST_FRAMEWORK_EXTENSIONS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_EDX_REST_FRAMEWORK_EXTENSIONS',
        settings.OPR_EDX_REST_FRAMEWORK_EXTENSIONS
    )

    settings.OPR_MODULESTORE = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_MODULESTORE',
        settings.OPR_MODULESTORE
    )

    settings.OPR_STUDENT_ACCOUNT_LIBRARY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_STUDENT_ACCOUNT_LIBRARY',
        settings.OPR_STUDENT_ACCOUNT_LIBRARY
    )

    settings.OPR_STUDENT_LIBRARY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_STUDENT_LIBRARY',
        settings.OPR_STUDENT_LIBRARY
    )

    settings.OPR_COURSE_API = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_API',
        settings.OPR_COURSE_API,
    )

    settings.OPR_SUPPORTED_TASKS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_SUPPORTED_TASKS',
        settings.OPR_SUPPORTED_TASKS
    )

    settings.OPR_GOOGLE_ANALYTICS_VIEW_ID = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_GOOGLE_ANALYTICS_VIEW_ID',
        settings.OPR_GOOGLE_ANALYTICS_VIEW_ID
    )

    settings.OPR_GOOGLE_ANALYTICS_CREDENTIALS = getattr(settings, 'AUTH_TOKENS', {}).get(
        'OPR_GOOGLE_ANALYTICS_CREDENTIALS',
        settings.OPR_GOOGLE_ANALYTICS_CREDENTIALS
    )

    settings.OPR_TIME_BETWEEN_SESSIONS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_TIME_BETWEEN_SESSIONS',
        settings.OPR_TIME_BETWEEN_SESSIONS
    )

    # Since the learning tracker report is not required for Juniper, this middleware has been disabled.
    # if settings.SERVICE_VARIANT == "lms":
    #     settings.MIDDLEWARE += [
    #         'openedx_pearson_reports.middleware.UserSessionMiddleware',
    #     ]

    settings.OPR_COURSE_DETAILS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_DETAILS',
        settings.OPR_COURSE_DETAILS
    )

    settings.OPR_COURSEWARE_LIBRARY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSEWARE_LIBRARY',
        settings.OPR_COURSEWARE_LIBRARY
    )

    settings.OPR_GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = getattr(settings, 'AUTH_TOKENS', {}).get(
        'OPR_GOOGLE_SERVICE_ACCOUNT_CREDENTIALS',
        settings.OPR_GOOGLE_SERVICE_ACCOUNT_CREDENTIALS,
    )

    settings.OPR_GOOGLE_CLOUD_PROJECT_ID = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_GOOGLE_CLOUD_PROJECT_ID',
        settings.OPR_GOOGLE_CLOUD_PROJECT_ID,
    )

    settings.OPR_GOOGLE_BIGQUERY_MAX_PROCESS_BYTES = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_GOOGLE_BIGQUERY_MAX_PROCESS_BYTES',
        settings.OPR_GOOGLE_BIGQUERY_MAX_PROCESS_BYTES,
    )

    settings.OPR_GOOGLE_BIGQUERY_MAX_NUMBER_RESULTS_PER_QUERY = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_GOOGLE_BIGQUERY_MAX_NUMBER_RESULTS_PER_QUERY',
        settings.OPR_GOOGLE_BIGQUERY_MAX_NUMBER_RESULTS_PER_QUERY,
    )

    settings.OPR_GOOGLE_BIGQUERY_USE_CACHE = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_GOOGLE_BIGQUERY_USE_CACHE',
        settings.OPR_GOOGLE_BIGQUERY_USE_CACHE,
    )

    settings.OPR_GOOGLE_BIGQUERY_TIME_ON_ASSET_DAILY_COLUMN_NAME = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_GOOGLE_BIGQUERY_TIME_ON_ASSET_DAILY_COLUMN_NAME',
        settings.OPR_GOOGLE_BIGQUERY_TIME_ON_ASSET_DAILY_COLUMN_NAME,
    )

    settings.OPR_SUPPORTED_REPORTS_BACKENDS = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_SUPPORTED_REPORTS_BACKENDS',
        settings.OPR_SUPPORTED_REPORTS_BACKENDS,
    )

    settings.OPR_DEFAULT_PAGE_RESULTS_LIMIT = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_DEFAULT_PAGE_RESULTS_LIMIT',
        settings.OPR_DEFAULT_PAGE_RESULTS_LIMIT,
    )

    settings.OPR_COURSE_CONTENT = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_COURSE_CONTENT',
        settings.OPR_COURSE_CONTENT,
    )

    settings.OPR_OPENEDX_AUTHENTICATION = getattr(settings, 'ENV_TOKENS', {}).get(
        'OPR_OPENEDX_AUTHENTICATION',
        settings.OPR_OPENEDX_AUTHENTICATION,
    )
