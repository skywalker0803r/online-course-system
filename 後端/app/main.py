import uuid

class Course:
    def __init__(self, name, description, max_attendees):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.max_attendees = max_attendees
        self.status = 'active'
        self.enrollments = [] # To track enrollments for deletion logic
        self.assigned_instructor = None

class User:
    def __init__(self, user_id):
        self.id = user_id
        self.enrolled_courses = []

class Enrollment:
    def __init__(self, user_id, course_id):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.course_id = course_id

class Instructor:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.schedule = [] # List of course IDs assigned to this instructor

class CourseManagementSystem:
    def __init__(self):
        self.courses = {}
        self.users = {}
        self.enrollments = {}
        self.instructors = {}

    def add_course(self, name, description, max_attendees):
        if name in self.courses:
            return None # Course with this name already exists
        new_course = Course(name, description, max_attendees)
        self.courses[name] = new_course
        return new_course

    def get_course(self, name):
        return self.courses.get(name)

    def update_course(self, name, new_description, new_max_attendees):
        course = self.get_course(name)
        if course:
            course.description = new_description
            course.max_attendees = new_max_attendees
            return course
        return None

    def delete_course(self, name):
        course = self.get_course(name)
        if course:
            if course.enrollments: # If there are enrollments, prevent deletion
                return False
            else:
                del self.courses[name]
                return True
        return False

    def get_all_courses(self):
        return list(self.courses.values())

    def get_course_details(self, name):
        return self.get_course(name)

    def enroll_course(self, user_id, course_name):
        course = self.get_course(course_name)
        if course:
            if user_id in course.enrollments: # Check if user is already enrolled
                return False
            if len(course.enrollments) < course.max_attendees:
                course.enrollments.append(user_id) # Simulate enrollment
                return True
            else:
                return False # Course is full
        return False

    def cancel_enrollment(self, user_id, course_name):
        course = self.get_course(course_name)
        if course:
            if user_id in course.enrollments:
                course.enrollments.remove(user_id)
                return True
            else:
                return False # User not enrolled
        return False

    def get_user_enrollments(self, user_id):
        user_enrollments = []
        for course in self.courses.values():
            if user_id in course.enrollments:
                user_enrollments.append(course)
        return user_enrollments

    def add_instructor(self, name):
        if name in self.instructors:
            return None
        new_instructor = Instructor(name)
        self.instructors[name] = new_instructor
        return new_instructor

    def get_instructor(self, name):
        return self.instructors.get(name)

    def assign_instructor(self, instructor_name, course_name):
        # This method will be implemented in the next step
        pass
