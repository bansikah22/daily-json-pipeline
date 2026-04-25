package com.example;

import java.time.LocalDateTime;

public record Product(
    String name,
    double price,
    String availability,
    double rating,
    LocalDateTime scrapedAt
) {}
