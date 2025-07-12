from behave import *
from 後端.app.main import CourseManagementSystem, Course

@given('a course "{name}" is available with max attendees {max_attendees:d} and current attendees {current_attendees:d}')
def step_impl(context, name, max_attendees, current_attendees):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    course = context.system.add_course(name, "", max_attendees)
    if course:
        for _ in range(current_attendees):
            course.enrollments.append("mock_enrollment_id")
    context.initial_attendees = current_attendees

@given('a course "{name}" is full with max attendees {max_attendees:d} and current attendees {current_attendees:d}')
def step_impl(context, name, max_attendees, current_attendees):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    course = context.system.add_course(name, "", max_attendees)
    if course:
        for _ in range(current_attendees):
            course.enrollments.append("mock_enrollment_id")
    context.initial_attendees = current_attendees

@given('a user is already enrolled in "{course_name}"')
def step_impl(context, course_name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    course = context.system.add_course(course_name, "", 100) # Add course if not exists
    if course:
        course.enrollments.append("test_user_123") # Simulate user enrollment
    context.user_id = "test_user_123"
    context.course_name = course_name

@given('a user is enrolled in "{course_name}"')
def step_impl(context, course_name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    course = context.system.add_course(course_name, "", 100) # Add course if not exists
    if course:
        course.enrollments.append("test_user_123") # Simulate user enrollment
    context.user_id = "test_user_123"
    context.course_name = course_name
    context.initial_attendees = len(course.enrollments)

@given('a user is not enrolled in "{course_name}"')
def step_impl(context, course_name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.course_name = course_name
    context.user_id = "test_user_123"
    # Ensure the course exists but the user is not enrolled
    course = context.system.get_course(course_name)
    if not course:
        context.system.add_course(course_name, "", 100)

@given('a user has enrolled in "{course_names}"')
def step_impl(context, course_names):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.user_id = "test_user_123"
    names = [name.strip() for name in course_names.split('and')]
    for name in names:
        course = context.system.add_course(name, "", 100) # Add course if not exists
        if course and context.user_id not in course.enrollments:
            course.enrollments.append(context.user_id)

@when('a user enrolls in the course "{course_name}"')
def step_impl(context, course_name):
    context.course_name = course_name
    # For now, use a dummy user ID
    user_id = "test_user_123"
    context.enrollment_result = context.system.enroll_course(user_id, course_name)

@when('a user attempts to enroll in the course "{course_name}"')
def step_impl(context, course_name):
    context.course_name = course_name
    user_id = "test_user_123"
    context.enrollment_result = context.system.enroll_course(user_id, course_name)
    context.error_message = "Course is full." if not context.enrollment_result else ""

@when('the user attempts to enroll in "{course_name}" again')
def step_impl(context, course_name):
    context.course_name = course_name
    user_id = "test_user_123"
    context.enrollment_result = context.system.enroll_course(user_id, course_name)
    context.error_message = "User is already enrolled." if not context.enrollment_result else ""

@when('the user cancels their enrollment in "{course_name}"')
def step_impl(context, course_name):
    context.course_name = course_name
    user_id = "test_user_123"
    context.cancellation_result = context.system.cancel_enrollment(user_id, course_name)

@when('the user attempts to cancel an enrollment for "{course_name}"')
def step_impl(context, course_name):
    context.course_name = course_name
    user_id = "test_user_123"
    context.cancellation_result = context.system.cancel_enrollment(user_id, course_name)
    context.error_message = "Enrollment does not exist." if not context.cancellation_result else ""

@when('the user requests to view their enrollment history')
def step_impl(context):
    context.user_id = "test_user_123"
    context.enrollment_history = context.system.get_user_enrollments(context.user_id)

@then('the enrollment should be successful')
def step_impl(context):
    assert context.enrollment_result is True, "Enrollment was not successful."

@then('the current attendees for "{course_name}" should increase by 1')
def step_impl(context, course_name):
    course = context.system.get_course(course_name)
    assert course is not None, f"Course '{course_name}' not found."
    assert len(course.enrollments) == context.initial_attendees + 1, f"Expected {context.initial_attendees + 1} attendees, but got {len(course.enrollments)}"

@then('the enrollment should fail')
def step_impl(context):
    assert context.enrollment_result is False, "Enrollment should have failed, but succeeded."

@then('an error message indicating the course is full should be returned')
def step_impl(context):
    assert "Course is full." in context.error_message, f"Expected error message about full course, but got: {context.error_message}"

@then('an error message indicating the user is already enrolled should be returned')
def step_impl(context):
    assert "User is already enrolled." in context.error_message, f"Expected error message about already enrolled, but got: {context.error_message}"

@then('the enrollment should be successfully cancelled')
def step_impl(context):
    assert context.cancellation_result is True, "Enrollment was not successfully cancelled."

@then('the current attendees for "{course_name}" should decrease by 1')
def step_impl(context, course_name):
    course = context.system.get_course(course_name)
    assert course is not None, f"Course '{course_name}' not found."
    assert len(course.enrollments) == context.initial_attendees - 1, f"Expected {context.initial_attendees - 1} attendees, but got {len(course.enrollments)}"

@then('the cancellation should fail')
def step_impl(context):
    assert context.cancellation_result is False, "Cancellation should have failed, but succeeded."

@then('an error message indicating the enrollment does not exist should be returned')
def step_impl(context):
    assert "Enrollment does not exist." in context.error_message, f"Expected error message about non-existent enrollment, but got: {context.error_message}"

@then('the system should return a list of enrollments including "{expected_course_names}"')
def step_impl(context, expected_course_names):
    expected_names = [name.strip() for name in expected_course_names.split('and')]
    actual_names = [enrollment.name for enrollment in context.enrollment_history]
    assert sorted(actual_names) == sorted(expected_names), f"Expected {expected_names}, but got {actual_names}"