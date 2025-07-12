import uuid

class Course:
    def __init__(self, name, description, max_attendees, start_time=None, end_time=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.max_attendees = max_attendees
        self.status = 'active'
        self.enrollments = [] # To track enrollments for deletion logic
        self.assigned_instructor = None
        self.start_time = start_time
        self.end_time = end_time

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
        self.schedule = [] # List of tuples: (course_name, start_time, end_time)

class CourseManagementSystem:
    def __init__(self):
        self.courses = {}
        self.users = {}
        self.enrollments = {}
        self.instructors = {}

    def add_course(self, name, description, max_attendees, start_time=None, end_time=None):
        if name in self.courses:
            return None # Course with this name already exists
        new_course = Course(name, description, max_attendees, start_time, end_time)
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

    def assign_instructor_to_course(self, instructor_name, course_name):
        course = self.get_course(course_name)
        instructor = self.get_instructor(instructor_name)
        if not course:
            raise ValueError("Course not found")
        if not instructor:
            raise ValueError("Instructor not found")
        
        if course.start_time and course.end_time and self.has_time_conflict(instructor_name, course.start_time, course.end_time):
            raise ValueError("Time conflict: Instructor is already busy during this time slot.")

        course.assigned_instructor = instructor_name
        instructor.schedule.append((course_name, course.start_time, course.end_time))
        return True

    def is_instructor_assigned_to_course(self, instructor_name, course_name):
        course = self.get_course(course_name)
        if course and course.assigned_instructor == instructor_name:
            return True
        return False

    def assign_instructor_to_course_with_adjustment(self, instructor_name, course_name):
        course = self.get_course(course_name)
        instructor = self.get_instructor(instructor_name)
        if not course:
            raise ValueError("Course not found")
        if not instructor:
            raise ValueError("Instructor not found")
        
        if course.start_time and course.end_time and self.has_time_conflict(instructor_name, course.start_time, course.end_time):
            original_start_time = course.start_time
            original_end_time = course.end_time

            new_start_time = str(int(original_start_time.split(':')[0]) + 1).zfill(2) + ':' + original_start_time.split(':')[1]
            new_end_time = str(int(original_end_time.split(':')[0]) + 1).zfill(2) + ':' + original_end_time.split(':')[1]

            if not self.has_time_conflict(instructor_name, new_start_time, new_end_time):
                course.start_time = new_start_time
                course.end_time = new_end_time
                course.assigned_instructor = instructor_name
                instructor.schedule.append((course_name, course.start_time, course.end_time))
                return True
            else:
                raise ValueError("No available slot: Instructor is busy and no alternative time slot found.")
        else:
            course.assigned_instructor = instructor_name
            instructor.schedule.append((course_name, course.start_time, course.end_time))
            return True

    def has_time_conflict(self, instructor_name, start_time, end_time):
        instructor = self.get_instructor(instructor_name)
        if not instructor:
            print(f"DEBUG: Instructor {instructor_name} not found for time conflict check.")
            return False
        
        def time_to_minutes(time_str):
            h, m = map(int, time_str.split(':'))
            return h * 60 + m

        new_start_minutes = time_to_minutes(start_time)
        new_end_minutes = time_to_minutes(end_time)

        print(f"DEBUG: Checking conflict for {instructor_name} with new slot {start_time}-{end_time} ({new_start_minutes}-{new_end_minutes} minutes)")
        for assigned_course_name, assigned_start_str, assigned_end_str in instructor.schedule:
            assigned_start_minutes = time_to_minutes(assigned_start_str)
            assigned_end_minutes = time_to_minutes(assigned_end_str)
            print(f"DEBUG:   Comparing with assigned slot {assigned_course_name} {assigned_start_str}-{assigned_end_str} ({assigned_start_minutes}-{assigned_end_minutes} minutes)")

            if (new_start_minutes < assigned_end_minutes and new_end_minutes > assigned_start_minutes):
                print("DEBUG:   Conflict detected!")
                return True # Conflict
        print("DEBUG: No conflict detected.")
        return False
