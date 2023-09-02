#!/bin/bash

# Copy files
cp -r ../cvf/src/ convform/src/

# Change directory
cd convform/

# Run 'maturin develop'
maturin develop

# Change back to the previous directory
cd ..

# Run 'python test.py'
python test.py

