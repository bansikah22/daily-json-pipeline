package com.example;

import java.io.IOException;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        ScraperService scraper = new ScraperService();
        JsonWriterService writer = new JsonWriterService();

        try {
            List<Product> products = scraper.scrapeProducts();
            writer.writeToFile(products);
            System.out.println("Successfully scraped " + products.size() + " products and wrote to file.");
        } catch (IOException e) {
            System.err.println("Error during scraping or writing: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
