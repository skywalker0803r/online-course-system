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

@when(u'an administrator assigns "{instructor_name}" to "{course_name}"')
def step_impl(context, instructor_name, course_name):
    context.system.assign_instructor_to_course(instructor_name, course_name)

@then(u'"{instructor_name}" should be successfully assigned to "{course_name}"')
def step_impl(context, instructor_name, course_name):
    assert context.system.is_instructor_assigned_to_course(instructor_name, course_name)
