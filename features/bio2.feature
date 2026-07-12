Feature: BIO2 compliance audit
  As an information security officer
  I want to know my organizations compliance status
  So that I know which measures are missing

  Background:
    Given the domain "bio2" is loaded

  Scenario: Compliance check returns total rule count
    When I run the BIO2 compliance check
    Then the total number of rules is 162
    And the compliance percentage is unavailable without evidence

  Scenario: Compliance check returns gaps
    When I run the BIO2 compliance check
    Then the result contains a list of gaps

  Scenario: Compliance check has domain metadata
    When I run the BIO2 compliance check
    Then the domain is "bio2"
    And the framework is "bio2"
