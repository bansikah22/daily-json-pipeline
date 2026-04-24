#!/bin/bash

# Script to run the Python consumer
# Assumes we're in the project root

cd consumer-python
source venv/bin/activate
python consumer.py
echo "Python consumer completed at $(date)"