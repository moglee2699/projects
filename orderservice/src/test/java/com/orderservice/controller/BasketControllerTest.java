package com.orderservice.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.orderservice.model.BasketItem;
import com.orderservice.service.BasketService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(BasketController.class)
class BasketControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private BasketService basketService;

    private BasketItem item;

    @BeforeEach
    void setUp() {
        item = new BasketItem("1", "Item1", 2);
    }

    @Test
    void testAddItem() throws Exception {
        mockMvc.perform(post("/basket/add")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(item)))
                .andExpect(status().isOk());
    }

    @Test
    void testViewBasket() throws Exception {
        when(basketService.getItems()).thenReturn(Arrays.asList(item));
        mockMvc.perform(get("/basket/view"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Item1"));
    }

    @Test
    void testRemoveItem() throws Exception {
        doNothing().when(basketService).removeItem("1");
        mockMvc.perform(delete("/basket/remove/1"))
                .andExpect(status().isOk());
    }

    @Test
    void testCheckout() throws Exception {
        doNothing().when(basketService).clearBasket();
        mockMvc.perform(post("/checkout"))
                .andExpect(status().isOk());
    }
}
