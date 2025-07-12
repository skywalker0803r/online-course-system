Feature: Instructor Scheduling and Assignment

  Scenario: Successfully assign an instructor to a course without conflict
    Given a course "History of Art" is available
    And an instructor "Dr. Smith" is available during the course time slot
    When an administrator assigns "Dr. Smith" to "History of Art"
    Then "Dr. Smith" should be successfully assigned to "History of Art"
    And the instructor's schedule should be updated

  Scenario: Attempt to assign an instructor to a non-existent course
    Given an instructor "Dr. Jones" is available
    When an administrator attempts to assign "Dr. Jones" to a non-existent course "Advanced Rocket Science"
    Then the assignment should fail
    And an error message indicating the course does not exist should be returned

  Scenario: Attempt to assign a non-existent instructor to a course
    Given a course "Introduction to AI" is available
    When an administrator attempts to assign a non-existent instructor "Dr. Who" to "Introduction to AI"
    Then the assignment should fail
    And an error message indicating the instructor does not exist should be returned

  Scenario: Attempt to assign an instructor with a time conflict
    Given a course "Data Structures" is scheduled from 10:00 to 12:00
    And an instructor "Dr. Brown" is already assigned to "Algorithms" from 11:00 to 13:00
    When an administrator attempts to assign "Dr. Brown" to "Data Structures"
    Then the assignment should fail
    And an error message indicating a time conflict should be returned

  Scenario: Assign instructor with automatic time slot adjustment (successful)
    Given a course "Machine Learning" is scheduled from 09:00 to 11:00
    And an instructor "Dr. White" is busy from 09:00 to 10:00
    When an administrator assigns "Dr. White" to "Machine Learning" and expects a successful adjustment
    Then the system should attempt to find an alternative time slot for "Machine Learning" with "Dr. White"
    And if a suitable alternative is found, "Dr. White" should be assigned to "Machine Learning" at the new time

  Scenario: Assign instructor with automatic time slot adjustment (no suitable alternative)
    Given a course "Advanced Machine Learning" is scheduled from 09:00 to 11:00
    And an instructor "Dr. White" is busy from 08:00 to 12:00
    When an administrator assigns "Dr. White" to "Advanced Machine Learning" and expects no suitable alternative
    Then the system should attempt to find an alternative time slot for "Advanced Machine Learning" with "Dr. White"
    And if no suitable alternative is found, an error message indicating no available slot should be returned
