Feature: Zorgtoeslag calculation
  As a citizen
  I want to know if I am entitled to healthcare benefit
  So that I can assess my financial situation

  Background:
    Given the domain "toeslagen" is loaded

  Scenario: Single person with income below threshold is entitled
    Given a single person of 30 years old
    And an annual income of 30000 euros
    When I calculate the healthcare benefit
    Then the entitlement is "true"
    And the amount is 123 euros per month
    And the source contains "Toeslagenwet"

  Scenario: Single person with income above threshold is not entitled
    Given a single person of 45 years old
    And an annual income of 40000 euros
    When I calculate the healthcare benefit
    Then the entitlement is "false"

  Scenario: Person younger than 18 is not entitled
    Given a single person of 16 years old
    And an annual income of 0 euros
    When I calculate the healthcare benefit
    Then the entitlement is "false"
