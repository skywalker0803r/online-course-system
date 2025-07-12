Feature: Course Enrollment and Inquiry

  Scenario: Enroll in an available course
    Given a course "Art History" is available with max attendees 20 and current attendees 5
    When a user enrolls in the course "Art History"
    Then the enrollment should be successful
    And the current attendees for "Art History" should increase by 1

  Scenario: Attempt to enroll in a full course
    Given a course "Advanced Chemistry" is full with max attendees 10 and current attendees 10
    When a user attempts to enroll in the course "Advanced Chemistry"
    Then the enrollment should fail
    And an error message indicating the course is full should be returned

  Scenario: Attempt to enroll in an already enrolled course
    Given a user is already enrolled in "Introduction to Philosophy"
    When the user attempts to enroll in "Introduction to Philosophy" again
    Then the enrollment should fail
    And an error message indicating the user is already enrolled should be returned

  Scenario: Cancel an existing enrollment
    Given a user is enrolled in "Linear Algebra"
    When the user cancels their enrollment in "Linear Algebra"
    Then the enrollment should be successfully cancelled
    And the current attendees for "Linear Algebra" should decrease by 1

  Scenario: Attempt to cancel a non-existent enrollment
    Given a user is not enrolled in "Quantum Physics"
    When the user attempts to cancel an enrollment for "Quantum Physics"
    Then the cancellation should fail
    And an error message indicating the enrollment does not exist should be returned

  Scenario: View user's enrollment history
    Given a user has enrolled in "Biology 101" and "Psychology Basics"
    When the user requests to view their enrollment history
    Then the system should return a list of enrollments including "Biology 101" and "Psychology Basics"
