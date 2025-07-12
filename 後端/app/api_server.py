
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add the parent directory to the sys.path to allow imports from main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import CourseManagementSystem, Course

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

cms = CourseManagementSystem()

# Sample data for demonstration
cms.add_course("Introduction to Python", "A beginner-friendly course on Python programming.", 30, "10:00", "12:00")
cms.add_course("Web Development with FastAPI", "Learn to build web APIs with FastAPI.", 25, "13:00", "15:00")
cms.add_instructor("John Doe")


class CourseCreate(BaseModel):
    name: str
    description: str
    max_attendees: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None

class CourseUpdate(BaseModel):
    description: str
    max_attendees: int

class EnrollmentRequest(BaseModel):
    user_id: str
    course_name: str

class InstructorRequest(BaseModel):
    instructor_name: str

class InstructorCreate(BaseModel):
    name: str

@app.post("/api/instructors", response_model=InstructorCreate)
def create_instructor(instructor: InstructorCreate):
    new_instructor = cms.add_instructor(instructor.name)
    if new_instructor is None:
        raise HTTPException(status_code=400, detail="Instructor with this name already exists")
    return instructor

@app.get("/api/instructors")
def get_instructors():
    return cms.get_all_instructors()

@app.post("/api/courses", response_model=CourseCreate)
def create_course(course: CourseCreate):
    new_course = cms.add_course(course.name, course.description, course.max_attendees, course.start_time, course.end_time)
    if new_course is None:
        raise HTTPException(status_code=400, detail="Course with this name already exists")
    return course

@app.get("/api/courses")
def get_courses():
    return cms.get_all_courses()

@app.get("/api/courses/{course_name}")
def get_course(course_name: str):
    course = cms.get_course_details(course_name)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/api/courses/{course_name}", response_model=CourseUpdate)
def update_course(course_name: str, course: CourseUpdate):
    updated_course = cms.update_course(course_name, course.description, course.max_attendees)
    if updated_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.delete("/api/courses/{course_name}")
def delete_course(course_name: str):
    if not cms.delete_course(course_name):
        raise HTTPException(status_code=400, detail="Course has enrollments or does not exist")
    return {"message": "Course deleted successfully"}

@app.post("/api/courses/{course_name}/enroll")
def enroll_course(course_name: str, enrollment: EnrollmentRequest):
    if not cms.enroll_course(enrollment.user_id, course_name):
        raise HTTPException(status_code=400, detail="Enrollment failed. Course might be full or user already enrolled.")
    return {"message": "Enrolled successfully"}

@app.post("/api/courses/{course_name}/cancel")
def cancel_enrollment(course_name: str, enrollment: EnrollmentRequest):
    if not cms.cancel_enrollment(enrollment.user_id, course_name):
        raise HTTPException(status_code=400, detail="Cancellation failed. User not enrolled or course does not exist.")
    return {"message": "Enrollment cancelled successfully"}

@app.get("/api/users/{user_id}/enrollments")
def get_user_enrollments(user_id: str):
    return cms.get_user_enrollments(user_id)

@app.post("/api/courses/{course_name}/assign_instructor")
def assign_instructor(course_name: str, instructor: InstructorRequest):
    try:
        cms.assign_instructor_to_course(instructor.instructor_name, course_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Instructor assigned successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
