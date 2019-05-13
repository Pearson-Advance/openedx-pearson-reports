"""
Task for Openedx Proversity Report plugin.
"""
from celery import task
from django.contrib.auth.models import User
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from openedx_proversity_reports.reports.last_page_accessed import (
    get_last_page_accessed_data,
    get_exit_count_data,
)
from openedx_proversity_reports.reports.time_spent_report import get_time_spent_report_data
from openedx_proversity_reports.utils import generate_report_as_list, get_root_block


@task(default_retry_delay=5, max_retries=5)  # pylint: disable=not-callable
def generate_completion_report(courses, block_report_filter):
    """
    Return the completion data for the given courses
    """
    data = {}
    for course_id in courses:
        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            continue

        # Getting all students enrolled on the course except staff users
        enrolled_students = User.objects.filter(
            courseenrollment__course_id=course_key,
            courseenrollment__is_active=1,
            is_staff=0,
        )

        staff_users = User.objects.filter(
            courseenrollment__course_id=course_key,
            courseenrollment__is_active=1,
            is_staff=1,
        )
        if not staff_users:
            break
        block_root = get_root_block(staff_users[0], course_key)
        course_data = generate_report_as_list(enrolled_students, course_key, block_report_filter, block_root)

        data[course_id] = course_data

    return data


@task(default_retry_delay=5, max_retries=5)  # pylint: disable=not-callable
def generate_last_page_accessed_report(courses):
    """
    Return the last page accessed data for the given courses.

    The dictionary contains 'last_page_data' that contains information about the last problem
    or html or video, etc, that user has accessed.
    exit_count_data holds information about all units in the course and the count of how many users are in each unit.
    """
    report_data = {
        'last_page_data': {},
        'exit_count_data': {},
    }

    last_page_data = get_last_page_accessed_data(courses)
    if last_page_data:
        report_data['last_page_data'] = last_page_data
        report_data['exit_count_data'] = get_exit_count_data(last_page_data, courses)

    return report_data


@task(default_retry_delay=5, max_retries=5)  # pylint: disable=not-callable
def generate_time_spent_report(courses):
    """
    Return the time spent data for the given courses.

    Args:
        courses: Course ids list.
    Returns:
        Dict with 'time_spent_data' containing time spent report data.
    """
    time_spent_report_data = get_time_spent_report_data(courses)

    return {
        'time_spent_data': time_spent_report_data if time_spent_report_data else {}
    }
