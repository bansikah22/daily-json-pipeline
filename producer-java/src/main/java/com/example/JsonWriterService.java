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

        String date = LocalDate.now().toString();
        String tempFileName = "products.json.tmp";
        String finalFileName = "products-" + date + ".json";
        Path tempPath = Paths.get("../shared-data/processed", tempFileName);
        Path finalPath = Paths.get("../shared-data/processed", finalFileName);

        File tempFile = tempPath.toFile();
        mapper.writeValue(tempFile, products);

        Files.move(tempPath, finalPath, StandardCopyOption.REPLACE_EXISTING);
    }
}
