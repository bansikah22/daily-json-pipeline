#!/bin/sh

# This script deletes files older than 30 days from the processed and reports directories.

PROCESSED_DIR="/data/processed"
REPORTS_DIR="/data/reports"
# Use RETENTION_DAYS from environment, or default to 30
RETENTION_DAYS=${RETENTION_DAYS:-30}

echo "Starting cleanup..."
echo "Retention policy: Deleting files older than $RETENTION_DAYS days."

# Find and delete old files in the processed directory
find $PROCESSED_DIR -type f -mtime +$RETENTION_DAYS -name "*.json" -print -delete

# Find and delete old files in the reports directory
find $REPORTS_DIR -type f -mtime +$RETENTION_DAYS -name "*.json" -print -delete

echo "Cleanup complete."
