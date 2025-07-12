from behave import *
from 後端.app.main import CourseManagementSystem

@given('the system is running')
def step_impl(context):
    context.system = CourseManagementSystem()

@given('a course "{name}" exists with description "{description}" and max attendees {max_attendees:d}')
def step_impl(context, name, description, max_attendees):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_course(name, description, max_attendees)

@given('a course "{name}" exists with no enrollments')
def step_impl(context, name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    context.system.add_course(name, "", 100) # Default description and max attendees

@given('a course "{name}" exists with existing enrollments')
def step_impl(context, name):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    course = context.system.add_course(name, "", 100)
    if course:
        course.enrollments.append("mock_enrollment_id") # Simulate an enrollment

@given('the system has courses "{course_names}"')
def step_impl(context, course_names):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    names = [name.strip() for name in course_names.split('and')]
    for name in names:
        context.system.add_course(name, "", 100) # Add courses with default values

@given('a course "{name}" exists with description "{description}" and {current_attendees:d} current attendees')
def step_impl(context, name, description, current_attendees):
    if not hasattr(context, 'system'):
        context.system = CourseManagementSystem()
    course = context.system.add_course(name, description, 100) # Max attendees can be default
    if course:
        # Simulate current attendees by adding mock enrollments
        for _ in range(current_attendees):
            course.enrollments.append("mock_enrollment_id")

@when('an administrator adds a new course with name "{name}", description "{description}", and max attendees {max_attendees:d}')
def step_impl(context, name, description, max_attendees):
    context.added_course = context.system.add_course(name, description, max_attendees)
    context.course_name = name
    context.course_description = description
    context.course_max_attendees = max_attendees

@when('an administrator updates the course "{name}" to have description "{new_description}" and max attendees {new_max_attendees:d}')
def step_impl(context, name, new_description, new_max_attendees):
    context.updated_course = context.system.update_course(name, new_description, new_max_attendees)
    context.course_name = name
    context.new_description = new_description
    context.new_max_attendees = new_max_attendees

@when('an administrator deletes the course "{name}"')
def step_impl(context, name):
    context.deleted_course_name = name
    context.delete_result = context.system.delete_course(name)

@when('an administrator attempts to delete the course "{name}"')
def step_impl(context, name):
    context.deleted_course_name = name
    context.delete_result = context.system.delete_course(name)
    context.error_message = "Course has existing enrollments and cannot be deleted." if not context.delete_result else ""

@when('a user requests to view all courses')
def step_impl(context):
    context.all_courses = context.system.get_all_courses()

@when('a user requests details for the course "{name}"')
def step_impl(context, name):
    context.requested_course_name = name
    context.course_details = context.system.get_course_details(name)

@then('the course "{name}" should be successfully created')
def step_impl(context, name):
    assert context.added_course is not None, f"Course '{name}' was not created."
    assert context.system.get_course(name) is not None, f"Course '{name}' not found in system."

@then('the course details should match the provided information')
def step_impl(context):
    created_course = context.system.get_course(context.course_name)
    assert created_course.name == context.course_name
    assert created_course.description == context.course_description
    assert created_course.max_attendees == context.course_max_attendees

@then('the course "{name}" should be successfully updated')
def step_impl(context, name):
    assert context.updated_course is not None, f"Course '{name}' was not successfully updated."

@then('its description should be "{expected_description}" and max attendees should be {expected_max_attendees:d}')
def step_impl(context, expected_description, expected_max_attendees):
    updated_course = context.system.get_course(context.course_name)
    assert updated_course.description == expected_description
    assert updated_course.max_attendees == expected_max_attendees

@then('the course "{name}" should be successfully deleted')
def step_impl(context, name):
    assert context.delete_result is True, f"Course '{name}' was not successfully deleted."

@then('it should no longer be available in the system')
def step_impl(context):
    assert context.system.get_course(context.deleted_course_name) is None, f"Course '{context.deleted_course_name}' is still available in the system."

@then('the system should prevent the deletion')
def step_impl(context):
    assert context.delete_result is False, "Course was deleted, but should have been prevented."

@then('an error message indicating existing enrollments should be returned')
def step_impl(context):
    assert "existing enrollments" in context.error_message, f"Expected error message about existing enrollments, but got: {context.error_message}"

@then('the system should return a list containing "{expected_course_names}"')
def step_impl(context, expected_course_names):
    expected_names = [name.strip() for name in expected_course_names.split('and')]
    actual_names = [course.name for course in context.all_courses]
    assert sorted(actual_names) == sorted(expected_names), f"Expected {expected_names}, but got {actual_names}"

@then('the system should return the details for "{name}"')
def step_impl(context, name):
    assert context.course_details is not None, f"No details returned for course '{name}'."
    assert context.course_details.name == name, f"Expected course name {name}, but got {context.course_details.name}"

@then('the description should be "{expected_description}" and current attendees should be {expected_attendees:d}')
def step_impl(context, expected_description, expected_attendees):
    assert context.course_details.description == expected_description, f"Expected description {expected_description}, but got {context.course_details.description}"
    assert len(context.course_details.enrollments) == expected_attendees, f"Expected {expected_attendees} attendees, but got {len(context.course_details.enrollments)}"
