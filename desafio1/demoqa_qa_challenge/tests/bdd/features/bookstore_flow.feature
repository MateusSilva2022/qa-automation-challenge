Feature: BookStore API flow

  Background:
    Given a new bookstore client

  Scenario: Successful end-to-end flow
    And random valid credentials
    When I create the user
    And I generate a token for the user
    Then the user is authorized
    When I list available books
    And I add two books to the user
    Then the user should contain those two books

  Scenario: Password rule is enforced
    And invalid credentials with password "abcd1234"
    When I try to create the user
    Then the response status should be 400
    And the error message should contain "Passwords must have"
