package com.orderservice.service;

import com.orderservice.model.BasketItem;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class BasketServiceTest {

    private BasketService basketService;

    @BeforeEach
    void setUp() {
        basketService = new BasketService();
    }

    @Test
    void testAddItem() {
        BasketItem item = new BasketItem("1", "Item1", 2);
        basketService.addItem(item);
        List<BasketItem> items = basketService.getItems();
        assertEquals(1, items.size());
        assertEquals("Item1", items.get(0).getName());
    }

    @Test
    void testRemoveItem() {
        BasketItem item = new BasketItem("1", "Item1", 2);
        basketService.addItem(item);
        basketService.removeItem("1");
        List<BasketItem> items = basketService.getItems();
        assertTrue(items.isEmpty());
    }

    @Test
    void testClearBasket() {
        basketService.addItem(new BasketItem("1", "Item1", 2));
        basketService.addItem(new BasketItem("2", "Item2", 3));
        basketService.clearBasket();
        assertTrue(basketService.getItems().isEmpty());
    }
}
