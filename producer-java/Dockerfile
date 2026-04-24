# Use Eclipse Temurin JDK 21
FROM eclipse-temurin:21-jdk

WORKDIR /app

COPY target/producer-java-1.0-SNAPSHOT.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]