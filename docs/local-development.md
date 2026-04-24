# Local Development Setup

This document explains how to run the daily data pipeline on your local machine using `docker-compose`.

## Prerequisites

- Java 21+
- Maven
- Python 3.12+
- Docker and `docker-compose`

## 1. Build the Java Producer

The Java application needs to be compiled and packaged into a `.jar` file before the Docker image can be built.

Navigate to the `producer-java` directory and run the Maven install command:

```bash
mvn install -f producer-java/pom.xml
```

This will create the `producer-java-1.0-SNAPSHOT.jar` file in the `producer-java/target` directory.

## 2. Run the Pipeline

The entire pipeline is managed by `docker-compose`. From the project root, run the following command:

```bash
docker-compose up --build
```

This command will:
1.  Build the Docker images for both the `java-scraper` and `python-consumer` services.
2.  Start the containers.
3.  The `python-consumer` will start and wait for a file to appear.
4.  The `java-scraper` will wait 5 seconds, then run, generating a JSON file in the `shared-data/incoming` directory.
5.  The `python-consumer` will detect the new file, process it, generate a report in `shared-data/reports`, move the source file to `shared-data/processed`, and then exit.

## Shared Data

The `shared-data` directory is mounted as a volume in both containers, allowing them to communicate by reading and writing files.

- `incoming/`: The Java scraper writes new JSON files here.
- `processed/`: The Python consumer moves files here after successful processing.
- `failed/`: The Python consumer moves files here if an error occurs.
- `reports/`: The Python consumer writes its analysis reports here.
