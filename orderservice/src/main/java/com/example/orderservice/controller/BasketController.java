package com.example.orderservice.controller;

import com.example.orderservice.model.BasketItem;
import com.example.orderservice.service.BasketService;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Collection;

@RestController
@RequestMapping("/basket")
public class BasketController {

    @Autowired
    private BasketService basketService;

    @Operation(summary = "Add item to basket")
    @PostMapping("/add")
    public String addItem(@RequestBody BasketItem item) {
        basketService.addItem(item);
        return "Item added to basket";
    }

    @Operation(summary = "View basket items")
    @GetMapping("/view")
    public Collection<BasketItem> viewBasket() {
        return basketService.viewItems();
    }

    @Operation(summary = "Remove item from basket by ID")
    @DeleteMapping("/remove/{id}")
    public String removeItem(@PathVariable String id) {
        return basketService.removeItem(id) ? "Item removed" : "Item not found";
    }

    @Operation(summary = "Checkout and clear basket")
    @PostMapping("/checkout")
    public String checkout() {
        double total = basketService.checkout();
        return "Checkout complete. Total amount: $" + total;
    }
}
