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

@when('an administrator assigns "{instructor_name}" to "{course_name}'')
def step_impl(context, instructor_name, course_name):
    context.instructor_name = instructor_name
    context.course_name = course_name
    context.assignment_result = None # This will be set by the actual method
    # This step will fail until the actual method is implemented
    assert False, f"Assignment of '{instructor_name}' to '{course_name}' was not attempted."

@then('"{instructor_name}" should be successfully assigned to "{course_name}'')
def step_impl(context, instructor_name, course_name):
    assert context.assignment_result is True, f"Expected '{instructor_name}' to be assigned to '{course_name}', but it failed."

@then('the instructor's schedule should be updated')
def step_impl(context):
    instructor = context.system.get_instructor(context.instructor_name)
    course = context.system.get_course(context.course_name)
    assert instructor is not None, f"Instructor '{context.instructor_name}' not found."
    assert course is not None, f"Course '{context.course_name}' not found."
    assert course.id in instructor.schedule, f"Instructor's schedule not updated for course '{course.name}'."
