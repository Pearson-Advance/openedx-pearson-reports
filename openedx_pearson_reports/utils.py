#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utils file for Openedx Pearson Reports.
"""
import copy
import logging
from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User

from openedx_pearson_reports.edxapp_wrapper.get_student_library import course_access_role, get_course_enrollment

logger = logging.getLogger(__name__)


def get_staff_user(course_key):
    """
    Returns the first staff user, to get the course structure.

    Args:
        course_key: Course key string.
    Returns:
        The first staff user of the course.
    """
    staff_user = User.objects.filter(
        courseenrollment__course_id=course_key,
        courseenrollment__is_active=1,
        courseaccessrole__role='staff',
    ).first()

    return staff_user


def get_user_role(user, course_key):
    """
    Returns the user string role.
    The default role value is 'student', other roles come from the course_access_role model.

    Args:
        user: Django user to find role.
        course_key: Course key string.
    Returns:
        The user role string.
    """
    user_role = 'student'
    user_course_role = course_access_role().objects.filter(
        user=user,
        course_id=course_key
    )

    if user_course_role:
        user_role = '-'.join([getattr(role, 'role', '') for role in user_course_role])

    return user_role


def get_enrolled_users(course_key, include_staff_users=False):
    """
    Return all the enrolled users for the given course key.

    Args:
        course_key: opaque_keys.edx.keys.CourseKey.
        include_staff_users: True to include course and platform staff users.
    Returns:
        Queryset of Users.
    """
    if include_staff_users:
        return User.objects.filter(
            courseenrollment__course_id=course_key,
            courseenrollment__is_active=1,
        )

    return User.objects.filter(
        courseenrollment__course_id=course_key,
        courseenrollment__is_active=1,
        courseaccessrole__id=None,
        is_staff=0,
    )


def get_attribute_from_module(module, attribute_name):
    """
    Return the attribute for the given module path and attribute name.

    Args:
        module: String (Module path).
        attribute_name: String (Module attribute).
    Returns:
        Module Attribute.
    """
    module = import_module(module)
    return getattr(module, attribute_name, None)


def get_exisiting_users_by_email(user_email_list):
    """
    Return a list of django.contrib.auth.models.User instances of users
    that exists in the platform.

    Args:
        user_email_list: List containing the emails of the users.
    Returns:
        exisiting_user_list: List containing django.contrib.auth.models.User instances.
    """
    exisiting_user_list = []

    for user_email in user_email_list:
        try:
            exisiting_user_list.append(User.objects.get(email=user_email))
        except User.DoesNotExist:
            continue

    return exisiting_user_list


def get_user_course_enrollments(user):
    """
    Return a list of course keys of the courses where the user is enrolled.

    Args:
        user: django.contrib.auth.models.User instance.
    Returns:
        List containing opaque_keys.edx.keys.CourseKey course instances.
    """
    course_enrollment_objects = get_course_enrollment().objects
    user_course_enrollments = course_enrollment_objects.filter(
        user__id=user.id,
        user__courseaccessrole__id=None,
    )

    return [course_enrollment.course_id for course_enrollment in user_course_enrollments]


def get_required_activity_dict(user_data):
    """
    Create a dict with the required activity data.

    Args:
        user_data: Activity completion report data per course.
    Returns:
        Dict containing activities info.
        {
            'Multiple Choice': 'completed',
            'Image Explorer': 'completed',
            'Video': 'not_completed'
        }
    """
    required_activities_data = {}
    total_activities = user_data.get('total_activities', 0)

    if total_activities:
        total = int(total_activities)
        # Create as many 'required_activity_' as the total number of activities.
        for activity_number in range(1, total + 1): # Plus 1, because the stop argument it's not inclusive.
            required_activity_status = user_data.get('required_activity_{}'.format(activity_number), 'not_completed')
            required_activity_name = user_data.get('required_activity_{}_name'.format(activity_number), '')

            # Let's add the activity number at the end of the name if two or more activities have the same name.
            if required_activity_name in required_activities_data.keys():
                required_activity_name = '{}-{}'.format(required_activity_name, activity_number)

            required_activities_data.update({
                required_activity_name: required_activity_status,
            })

    return required_activities_data


def get_report_backend(requested_report_name):
    """
    Return the correspondent report backend for the requested report.

    Args:
        requested_report_name: Name of the requested report.
    """
    report_name = requested_report_name.replace('-', '_')
    supported_backend_reports = getattr(settings, 'OPR_SUPPORTED_REPORTS_BACKENDS', {})

    if not (supported_backend_reports and report_name in supported_backend_reports):
        logging.error(
            'Either OPR_SUPPORTED_REPORTS_BACKENDS was not provided or the report backend was not configured.',
        )
        return None

    report_backend_settings = supported_backend_reports.get(report_name, {})
    report_backend_value = report_backend_settings.get('backend', '').split(':')

    try:
        backend_module = import_module(report_backend_value[0])
        report_backend = getattr(backend_module, report_backend_value[-1], None)
    except IndexError:
        logging.error('Report backend not found. %s', report_backend_value)
        report_backend = None

    return report_backend, report_backend_settings
