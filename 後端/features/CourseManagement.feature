Feature: Course Management

  Scenario: Add a new course
    Given the system is running
    When an administrator adds a new course with name "Introduction to Python", description "Learn Python basics", and max attendees 50
    Then the course "Introduction to Python" should be successfully created
    And the course details should match the provided information

  Scenario: Update course information
    Given a course "Python Advanced" exists with description "Advanced Python topics" and max attendees 30
    When an administrator updates the course "Python Advanced" to have description "Master Python" and max attendees 40
    Then the course "Python Advanced" should be successfully updated
    And its description should be "Master Python" and max attendees should be 40

  Scenario: Delete a course without enrollments
    Given a course "Data Science Fundamentals" exists with no enrollments
    When an administrator deletes the course "Data Science Fundamentals"
    Then the course "Data Science Fundamentals" should be successfully deleted
    And it should no longer be available in the system

  Scenario: Attempt to delete a course with existing enrollments
    Given a course "Web Development" exists with existing enrollments
    When an administrator attempts to delete the course "Web Development"
    Then the system should prevent the deletion
    And an error message indicating existing enrollments should be returned

  Scenario: Get all courses
    Given the system has courses "Math Basics" and "Physics 101"
    When a user requests to view all courses
    Then the system should return a list containing "Math Basics" and "Physics 101"

  Scenario: Get details of a specific course
    Given a course "Calculus I" exists with description "Single variable calculus" and 15 current attendees
    When a user requests details for the course "Calculus I"
    Then the system should return the details for "Calculus I"
    And the description should be "Single variable calculus" and current attendees should be 15
