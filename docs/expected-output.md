# Expected Output

When the pipeline runs successfully, you can expect to see the following output in the logs for the respective jobs.

## Java Scraper

The log from the `java-scraper` pod will show a simple success message indicating that it has generated the JSON file.

```
Successfully scraped 20 products and wrote to file.
```

## Python Consumer

The log from the `python-consumer` pod will show the steps it takes to process the file.

```
2026-04-24 14:55:01 - Starting consumer...
2026-04-24 14:55:01 - Analyzing /app/shared-data/incoming/products-2026-04-24.json
2026-04-24 14:55:01 - Analysis report saved to /app/shared-data/reports/products-2026-04-24_report.json
2026-04-24 14:55:01 - Moved 1 files to /app/shared-data/processed
2026-04-24 14:55:01 - Consumer finished.
```

## Shared Data Directory

After a successful run, you can inspect the shared data volume. You would typically do this by exec-ing into a pod, but for local testing, you can inspect the `shared-data` directory on your machine.

-   The `incoming/` directory should be empty.
-   The `processed/` directory should contain the `products-*.json` file.
-   The `reports/` directory should contain the `products-*_report.json` file.
