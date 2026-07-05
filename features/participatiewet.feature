Feature: Benefit eligibility check
  As a citizen
  I want to know if I am entitled to social assistance
  So that I know if I can apply for provisions

  Background:
    Given the domain "participatiewet" is loaded

  Scenario: Single parent with children is entitled
    Given a single parent of 40 years old
    And an annual income of 0 euros
    When I calculate the social assistance
    Then the result is not empty
