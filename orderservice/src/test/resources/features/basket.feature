Feature: Basket Management

  Scenario: Add item to basket
    Given the basket is empty
    When I add an item with id "1", name "Item1", and quantity 2
    Then the basket should contain 1 item

  Scenario: Remove item from basket
    Given the basket has an item with id "1"
    When I remove the item with id "1"
    Then the basket should be empty
