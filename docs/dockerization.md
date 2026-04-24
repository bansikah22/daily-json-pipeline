# Dockerization

Both the Java producer and the Python consumer are containerized using Docker. This ensures a consistent environment for development, testing, and production.

## Java Producer (`producer-java/Dockerfile`)

The Java application is a standalone `.jar` file. The Dockerfile is simple:

```dockerfile
# Use Eclipse Temurin JDK 21
FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY target/producer-java-1.0-SNAPSHOT.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
```

-   **`FROM eclipse-temurin:21-jdk`**: Starts from a base image with Java 21 installed.
-   **`WORKDIR /app`**: Sets the working directory inside the container to `/app`.
-   **`COPY target/producer-java-1.0-SNAPSHOT.jar app.jar`**: Copies the compiled `.jar` file (created by Maven) into the container and renames it to `app.jar`.
-   **`ENTRYPOINT ["java", "-jar", "app.jar"]`**: Specifies the command to run when the container starts.

## Python Consumer (`consumer-python/Dockerfile`)

The Python application has dependencies listed in `requirements.txt`.

```dockerfile
# Use Python 3.12
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "consumer.py"]
```

-   **`FROM python:3.12-slim`**: Starts from a lightweight Python 3.12 image.
-   **`WORKDIR /app`**: Sets the working directory to `/app`.
-   **`COPY requirements.txt .`**: Copies the requirements file into the container.
-   **`RUN pip install ...`**: Installs the Python dependencies.
-   **`COPY . .`**: Copies the rest of the consumer application code (e.g., `consumer.py`, `analyzer.py`) into the container.
-   **`CMD ["python", "consumer.py"]`**: Sets the default command to run when the container starts.
