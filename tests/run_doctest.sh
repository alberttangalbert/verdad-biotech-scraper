#!/bin/bash

# Shell script to run doctests on a Python script
# Usage: ./run_doctest.sh your_script.py

# Check if a script file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <python_script>"
    exit 1
fi

# Run the doctests
echo "Running doctests on $1..."
python -m doctest -v "$1"

# Check the exit status of doctest
if [ $? -eq 0 ]; then
    echo "Doctests passed successfully!"
else
    echo "Doctests failed!"
    exit 1
fi
