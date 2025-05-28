package com.orderservice.cucumber;

import com.orderservice.model.BasketItem;
import com.orderservice.service.BasketService;
import io.cucumber.java.en.*;
import static org.junit.jupiter.api.Assertions.*;

public class BasketStepDefinitions {

    private BasketService basketService;
    private BasketItem item;

    @Given("the basket is empty")
    public void the_basket_is_empty() {
        basketService = new BasketService();
    }

    @When("I add an item with id {string}, name {string}, and quantity {int}")
    public void i_add_an_item(String id, String name, Integer quantity) {
        item = new BasketItem(id, name, quantity);
        basketService.addItem(item);
    }

    @Then("the basket should contain {int} item")
    public void the_basket_should_contain_item(Integer count) {
        assertEquals(count, basketService.getItems().size());
    }

    @Given("the basket has an item with id {string}")
    public void the_basket_has_an_item(String id) {
        basketService = new BasketService();
        basketService.addItem(new BasketItem(id, "Item1", 2));
    }

    @When("I remove the item with id {string}")
    public void i_remove_the_item(String id) {
        basketService.removeItem(id);
    }

    @Then("the basket should be empty")
    public void the_basket_should_be_empty() {
        assertTrue(basketService.getItems().isEmpty());
    }
}
