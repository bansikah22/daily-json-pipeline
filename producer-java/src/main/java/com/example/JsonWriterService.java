package com.example;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDate;
import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

public class JsonWriterService {

    public void writeToFile(List<Product> products) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());

        String timestamp = java.time.format.DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss").format(java.time.LocalDateTime.now());
        String tempFileName = "products.json.tmp";
        String finalFileName = "products-" + timestamp + ".json";
        Path tempPath = Paths.get("/app/shared-data/incoming", tempFileName);
        Path finalPath = Paths.get("/app/shared-data/incoming", finalFileName);

        File tempFile = tempPath.toFile();
        mapper.writeValue(tempFile, products);

        Files.move(tempPath, finalPath, StandardCopyOption.REPLACE_EXISTING);
    }
}
