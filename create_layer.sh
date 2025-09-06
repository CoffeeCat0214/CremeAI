#!/bin/bash

# Create PyNaCl Lambda layer
cd layers/pynacl
zip -r ../../pynacl-layer.zip python/
cd ../..

echo "PyNaCl layer created: pynacl-layer.zip"
