package com.example;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class ScraperService {

    public List<Product> scrapeProducts() throws IOException {
        List<Product> products = new ArrayList<>();

        // Scrape from a demo website (books.toscrape.com)
        Document doc = Jsoup.connect("http://books.toscrape.com/").get();
        Elements productElements = doc.select(".product_pod");

        for (Element productElement : productElements) {
            String name = productElement.select("h3 a").attr("title");
            String priceText = productElement.select(".price_color").text();
            double price = Double.parseDouble(priceText.replace("£", ""));
            String availability = productElement.select(".instock").text().trim();
            // Rating is in class like "star-rating One", etc.
            String ratingClass = productElement.select(".star-rating").attr("class");
            double rating = parseRating(ratingClass);

            Product product = new Product(
                name,
                price,
                availability,
                rating,
                LocalDateTime.now()
            );

            products.add(product);
        }

        return products;
    }

    private double parseRating(String ratingClass) {
        if (ratingClass.contains("One")) return 1.0;
        if (ratingClass.contains("Two")) return 2.0;
        if (ratingClass.contains("Three")) return 3.0;
        if (ratingClass.contains("Four")) return 4.0;
        if (ratingClass.contains("Five")) return 5.0;
        return 0.0;
    }
}
