#!/bin/bash
# This script provides a simple way to test the full data pipeline locally.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- 0. Checking for .env file ---"
if [ ! -f .env ]; then
    echo "ERROR: .env file not found."
    echo "Please create one by copying the example:"
    echo "  cp .env.example .env"
    echo "Then, edit the .env file with your SMTP credentials."
    exit 1
fi
echo ".env file found. Proceeding with test."

echo "--- 1. Compiling Java producer ---"
mvn install -f producer-java/pom.xml

echo "\n--- 2. Building Docker images ---"
docker-compose build

# Clean up previous run's data to ensure a fresh start
echo "\n--- 3. Cleaning up previous run data ---"
rm -rf shared-data/incoming/*
rm -rf shared-data/processed/*
rm -rf shared-data/reports/*
rm -rf shared-data/failed/*
# Create directories if they don't exist
mkdir -p shared-data/incoming shared-data/processed shared-data/reports shared-data/failed

echo "\n--- 4. Running the pipeline ---"
# We will run the producer twice to test the comparison logic in the consumer
echo "--- Running producer (first run)..."
docker-compose run --rm java-scraper

# Wait a moment to ensure a different timestamp
sleep 2

echo "\n--- Running producer and consumer (second run)..."
docker-compose run --rm java-scraper
docker-compose run --rm python-consumer

echo "\n--- 5. Pipeline run finished ---"
echo "Check the 'shared-data' directory for results and your email for a notification."
