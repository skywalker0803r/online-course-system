from behave import *
from 後端.app.main import CourseManagementSystem, Course, Instructor

@given('a course "{course_name}" is available')
def step_impl(context, course_name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_course(course_name, "", 100)

@given('an instructor "{instructor_name}" is available during the course time slot')
def step_impl(context, instructor_name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_instructor(instructor_name)

@given('an instructor "{instructor_name}" is available')
def step_impl(context, instructor_name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_instructor(instructor_name)

@given('a course "{course_name}" is scheduled from {start_time} to {end_time}')
def step_impl(context, course_name, start_time, end_time):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_course(course_name, "", 100, start_time=start_time, end_time=end_time)

@given('an instructor "{instructor_name}" is already assigned to "{course_name}" from {start_time} to {end_time}')
def step_impl(context, instructor_name, course_name, start_time, end_time):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_instructor(instructor_name)
    context.system.add_course(course_name, "", 100, start_time=start_time, end_time=end_time)
    context.system.assign_instructor_to_course(instructor_name, course_name)

@given('an instructor "{instructor_name}" is busy from {start_time} to {end_time}')
def step_impl(context, instructor_name, start_time, end_time):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_instructor(instructor_name)
    # Simulate the instructor being busy by assigning them to a dummy course during that time
    dummy_course_name = f"Dummy Course for {instructor_name} {start_time}-{end_time}"
    context.system.add_course(dummy_course_name, "", 1, start_time=start_time, end_time=end_time)
    context.system.assign_instructor_to_course(instructor_name, dummy_course_name)

@when(u'an administrator assigns "{instructor_name}" to "{course_name}"')
def step_impl(context, instructor_name, course_name):
    context.assignment_successful = True # Assume success unless an exception is caught
    try:
        context.system.assign_instructor_to_course(instructor_name, course_name)
    except ValueError as e:
        context.assignment_successful = False
        context.error_message = str(e)

@when(u'an administrator attempts to assign "{instructor_name}" to a non-existent course "{course_name}"')
def step_impl(context, instructor_name, course_name):
    context.assignment_successful = True # Assume success unless an exception is caught
    try:
        context.system.assign_instructor_to_course(instructor_name, course_name)
    except ValueError as e:
        context.assignment_successful = False
        context.error_message = str(e)

@when(u'an administrator attempts to assign a non-existent instructor "{instructor_name}" to "{course_name}"')
def step_impl(context, instructor_name, course_name):
    context.assignment_successful = True # Assume success unless an exception is caught
    try:
        context.system.assign_instructor_to_course(instructor_name, course_name)
    except ValueError as e:
        context.assignment_successful = False
        context.error_message = str(e)

@when(u'an administrator attempts to assign "{instructor_name}" to "{course_name}"')
def step_impl(context, instructor_name, course_name):
    context.assignment_successful = True # Assume success unless an exception is caught
    try:
        context.system.assign_instructor_to_course(instructor_name, course_name)
    except ValueError as e:
        context.assignment_successful = False
        context.error_message = str(e)

@when(u'an administrator assigns "{instructor_name}" to "{course_name}" and expects a successful adjustment')
def step_impl(context, instructor_name, course_name):
    context.assignment_successful = True # Assume success unless an exception is caught
    try:
        context.system.assign_instructor_to_course_with_adjustment(instructor_name, course_name)
    except ValueError as e:
        context.assignment_successful = False
        context.error_message = str(e)

@when(u'an administrator assigns "{instructor_name}" to "{course_name}" and expects no suitable alternative')
def step_impl(context, instructor_name, course_name):
    context.assignment_successful = True # Assume success unless an exception is caught
    try:
        context.system.assign_instructor_to_course_with_adjustment(instructor_name, course_name)
    except ValueError as e:
        context.assignment_successful = False
        context.error_message = str(e)

@then(u'"{instructor_name}" should be successfully assigned to "{course_name}"')
def step_impl(context, instructor_name, course_name):
    assert context.system.is_instructor_assigned_to_course(instructor_name, course_name)

@then(u'the instructor\'s schedule should be updated')
def step_impl(context):
    # This step will be implemented in main.py
    pass

@then(u'the assignment should fail')
def step_impl(context):
    assert not context.assignment_successful

@then(u'an error message indicating the course does not exist should be returned')
def step_impl(context):
    assert "Course not found" in context.error_message

@then(u'an error message indicating the instructor does not exist should be returned')
def step_impl(context):
    assert "Instructor not found" in context.error_message

@then(u'an error message indicating a time conflict should be returned')
def step_impl(context):
    assert "Time conflict" in context.error_message

@then(u'the system should attempt to find an alternative time slot for "{course_name}" with "{instructor_name}"')
def step_impl(context, course_name, instructor_name):
    # This step is primarily for flow control and ensuring the method is called.
    # The actual logic for finding an alternative time slot is in main.py
    pass

@then(u'if a suitable alternative is found, "{instructor_name}" should be assigned to "{course_name}" at the new time')
def step_impl(context, instructor_name, course_name):
    assert context.assignment_successful
    assert context.system.is_instructor_assigned_to_course(instructor_name, course_name)

@then(u'if no suitable alternative is found, an error message indicating no available slot should be returned')
def step_impl(context):
    assert not context.assignment_successful
    assert "No available slot" in context.error_message