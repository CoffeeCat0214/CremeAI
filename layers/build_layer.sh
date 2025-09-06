#!/bin/bash

echo "Building PyNaCl layer for Lambda using Docker..."

# Build the Docker image
docker build -t pynacl-layer-builder .

echo "Extracting PyNaCl from Docker container..."

# Create a container and copy the python directory
docker create --name temp-container pynacl-layer-builder
docker cp temp-container:/opt/python ./python
docker rm temp-container

echo "Creating layer zip file..."

# Create the layer zip
cd python
zip -r ../pynacl-layer-linux.zip .
cd ..

echo "PyNaCl layer created: pynacl-layer-linux.zip"
echo "Layer size: $(du -h pynacl-layer-linux.zip | cut -f1)"