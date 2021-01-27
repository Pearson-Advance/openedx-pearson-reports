"""
Completion report backend.
"""
import copy
from importlib import import_module

from openedx_pearson_reports.edxapp_wrapper.get_completion_models import get_block_completion_model
from openedx_pearson_reports.edxapp_wrapper.get_course_api import get_supported_fields
from openedx_pearson_reports.edxapp_wrapper.get_course_blocks import get_course_blocks
from openedx_pearson_reports.edxapp_wrapper.get_course_cohort import get_course_cohort
from openedx_pearson_reports.edxapp_wrapper.get_course_teams import get_course_teams
from openedx_pearson_reports.edxapp_wrapper.get_modulestore import get_modulestore
from openedx_pearson_reports.reports.backend.base import BaseReportBackend
from openedx_pearson_reports.utils import get_exisiting_users_by_email

SUPPORTED_TASKS_MODULE = 'openedx_pearson_reports.tasks'
BLOCK_DEFAULT_REPORT_FILTER = ['vertical']

class CompletionReportBackend(BaseReportBackend):
    """
    Completion report backend class.
    """
    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        # Import the task module directly to avoid circular import.
        super(CompletionReportBackend, self).__init__(
            generate_report_data_task=getattr(
                import_module(SUPPORTED_TASKS_MODULE),
                'generate_completion_report_task',
                None,
            ),
            user_serializer_fields=['email'],
            include_staff_users=False,
            *args,
            **kwargs
        )

    def process_request(self, request, extra_data={}):  # pylint: disable=dangerous-default-value
        """
        Process the completion report request.

        Args:
            request: django.http.request.HttpRequest object.
            extra_data: Dict that contains additional data.
        Returns:
            BaseReportBackend.process_response object.
        """
        block_report_filter = extra_data.get('block_report_filter', BLOCK_DEFAULT_REPORT_FILTER)

        extra_data.update({'block_report_filter': block_report_filter})

        return super(CompletionReportBackend, self).process_request(request, extra_data)


def generate_completion_report(course_key, enrolled_users, block_report_filter):
    """
    Return the report data.

    Args:
        course_key: Opaque course key object.
        enrolled_users: List that contains information about the enrolled users.
        block_report_filter: Block type name to filter the report. e.g. vertical, chapter...
    Returns:
        List of dicts: [{
            cohort: User cohort name.
            block-type: {
                name: Display name of the block.
                section_name: Display name of the section.
                subsection_name: Display name of the subsection.
                subsection_number: Subsection place value.
                number: Block place value.
                complete: Completion value, true or false.
                section_number: Section place value.
            }
            team: User team name.
            user_id: User id value.
            username: Username value.
        }]
    """
    enrolled_users_objects = get_exisiting_users_by_email(
        user_email_list=(user.get('email', '') for user in enrolled_users),
    )

    if not enrolled_users_objects:
        return {}

    return generate_report_as_list(
        users=enrolled_users_objects,
        course_key=course_key,
        block_report_filter=block_report_filter,
        root_block=get_root_block(enrolled_users_objects[0], course_key),
    )


def generate_report_as_list(users, course_key, block_report_filter, root_block):
    """
    Returns a list with the user information for every block in block_report_filter.
    """

    def update_user_dict(child, user_data, section=None, subsection=None, vertical=None):
        """
        Returns the complete data for the given values.
        """
        if child.get('type') in block_report_filter:

            type_data = user_data.get(child.get('type'), [])

            child_data = dict(
                name=child.get('display_name'),
                complete=child.get('complete'),
                number=child.get('position_number'),
            )

            if section and section != child:
                child_data['section_name'] = section.get('display_name')
                child_data['section_number'] = section.get('position_number')

            if subsection and subsection != child:
                child_data['subsection_name'] = subsection.get('display_name')
                child_data['subsection_number'] = subsection.get('position_number')

            if vertical and vertical != child:
                child_data['vertical_name'] = vertical.get('display_name')
                child_data['vertical_number'] = vertical.get('position_number')

            type_data.append(child_data)

            user_data[child.get('type')] = type_data

    data = []
    for user in users:
        block_data = copy.deepcopy(root_block)
        mark_blocks_completed(block_data, user, course_key)
        sections = block_data.get('children', [])
        cohort = get_course_cohort(user=user, course_key=course_key)
        user_teams = get_course_teams(membership__user=user, course_id=course_key)

        user_data = dict(
            username=user.username,
            user_id=user.id,
            cohort=cohort.name if cohort else '',
            team=user_teams[0].name if user_teams else '',
        )

        for section in sections:
            update_user_dict(section, user_data)
            for subsection in section.get('children', []):
                update_user_dict(subsection, user_data, section)
                for vertical in subsection.get('children', []):
                    update_user_dict(vertical, user_data, section, subsection)
                    for component in vertical.get('children', []):
                        update_user_dict(component, user_data, section, subsection, vertical)

        data.append(user_data)

    return data


def get_root_block(user, course_key):
    """
    Returns the content course as dict.
    """

    def populate_children(block, all_blocks, counter={}):
        """
        Replace each child id with the full block for the child.

        Given a block, replaces each id in its children array with the full
        representation of that child, which will be looked up by id in the
        passed all_blocks dict. Recursively do the same replacement for children
        of those children.
        """
        children = block.get('children', [])
        block_type = block.get("type")

        if block_type:
            counter[block_type] = counter.get(block_type, -1) + 1
            block['position_number'] = counter[block_type]

        for i in range(len(children)):
            child_id = block['children'][i]
            child_detail = populate_children(all_blocks[child_id], all_blocks, counter)
            block['children'][i] = child_detail

        return block

    block_types_filter = [
        'course',
        'chapter',
        'sequential',
        'vertical',
        'html',
        'problem',
        'video',
        'discussion',
        'drag-and-drop-v2',
        'poll',
        'word_cloud'
    ]

    requested_fields = [
        'children',
        'display_name',
        'type',
        'due',
        'graded',
        'format'
    ]

    usage_key = get_modulestore().make_course_usage_key(course_key)
    blocks = get_course_blocks(user, usage_key)

    if block_types_filter:
        block_keys_to_remove = []
        for block_key in blocks:
            block_type = blocks.get_xblock_field(block_key, 'category')
            if block_type not in block_types_filter:
                block_keys_to_remove.append(block_key)
        for block_key in block_keys_to_remove:
            blocks.remove_block(block_key, keep_descendants=True)

    block_data = {}

    for block_key in blocks:
        block = {
            'block_key': block_key,
            'id': str(block_key),
            'block_id': str(block_key.block_id),
            'resume_block': False,
            'complete': False
        }
        for supported_field in get_supported_fields():
            if supported_field.requested_field_name in requested_fields:
                field_value = blocks.get_xblock_field(block_key, supported_field.block_field_name)
                if field_value:
                    # only return fields that have data
                    block[supported_field.serializer_field_name] = field_value

        children = blocks.get_children(block_key)
        if children:
            block['children'] = [str(child) for child in children]

        block_data[str(block_key)] = block

    root_block = populate_children(block_data[str(blocks.root_block_usage_key)], block_data)

    return root_block


def mark_blocks_completed(block, user, course_key):
    """
    Walk course tree, marking block completion.
    Mark 'most recent completed block as 'resume_block'
    """
    last_completed_child_position = get_block_completion_model().get_latest_block_completed(user, course_key)

    if last_completed_child_position:
        recurse_mark_complete(
            course_block_completions=get_block_completion_model().get_learning_context_completions(user, course_key),
            latest_completion=last_completed_child_position,
            block=block
        )


def recurse_mark_complete(course_block_completions, latest_completion, block):
    """
    Helper function to walk course tree dict,
    marking blocks as 'complete' and 'last_complete'

    If all blocks are complete, mark parent block complete
    mark parent blocks of 'last_complete' as 'last_complete'
    """
    block_key = block.get('block_key')

    if course_block_completions.get(block_key):
        block['complete'] = True
        if block_key == latest_completion.block_key:
            block['resume_block'] = True

    if block.get('children'):
        for idx in range(len(block['children'])):
            recurse_mark_complete(
                course_block_completions,
                latest_completion,
                block=block['children'][idx]
            )
            if block['children'][idx]['resume_block'] is True:
                block['resume_block'] = True

        completable_blocks = [child for child in block['children'] if child['type'] != 'discussion']
        if len([child['complete'] for child in block['children'] if child['complete']]) == len(completable_blocks):
            block['complete'] = True
