#!/bin/bash
# Deployment script for Neural Machine Translation API

echo "Building Docker image..."
docker build -t nm-translation-api .

echo "Running Docker container..."
docker run -d -p 8000:8000 --name nm-translation nm-translation-api

echo "API is running on http://localhost:8000"
echo "View API documentation at http://localhost:8000/docs"
