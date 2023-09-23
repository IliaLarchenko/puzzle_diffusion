#!/bin/bash

# Check if python3 is installed
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but it's not installed. Aborting."; exit 1; }

# Check if virtualenv is installed
command -v virtualenv >/dev/null 2>&1 || { echo >&2 "virtualenv is required but it's not installed. Installing..."; pip3 install virtualenv; }

# Create a virtual environment named .venv
virtualenv .venv -p python3

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages from requirements.txt
pip install -r requirements.txt

# Check for CUDA
if command -v nvcc &> /dev/null
then
    echo "CUDA is available on your system. You may want to set \"device\": \"cuda\" in your config."
else
    echo "CUDA is not available on your system."
fi

# Check for MPS (Only for MacOS)
if [ "$(uname)" == "Darwin" ]; then
    echo "You are running MacOS. You may want to consider using MPS by setting \"device\": \"mps\" in your config."
fi

# Run test.py
python test.py

# Deactivate the virtual environment
deactivate

echo "Setup completed successfully!"
