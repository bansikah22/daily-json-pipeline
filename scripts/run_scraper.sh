#!/bin/bash

# Script to run the Java scraper
# Assumes we're in the project root

cd producer-java
java -jar target/producer-java-1.0-SNAPSHOT.jar
echo "Java scraper completed at $(date)"