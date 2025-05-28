package com.example.orderservice.service;

import com.example.orderservice.model.BasketItem;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class BasketService {
    private final Map<String, BasketItem> basket = new HashMap<>();

    public void addItem(BasketItem item) {
        basket.put(item.getId(), item);
    }

    public Collection<BasketItem> viewItems() {
        return basket.values();
    }

    public boolean removeItem(String id) {
        return basket.remove(id) != null;
    }

    public double checkout() {
        double total = basket.values().stream()
                .mapToDouble(item -> item.getPrice() * item.getQuantity())
                .sum();
        basket.clear(); // empty the basket after checkout
        return total;
    }
}
