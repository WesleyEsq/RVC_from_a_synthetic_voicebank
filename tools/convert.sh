#!/bin/bash

echo "Installing dependencies...."

sudo dnf install nodejs

echo " Done! Now to execute the convertion from the pth to onnx..."
echo " "

# Ensure correct usage
if [ "$#" -ne 2 ]; then
    echo "Usage: ./convert.sh <input.pth> <output.onnx>"
    exit 1
fi

# Convert paths to absolute paths so they don't break when we change directories
INPUT_FILE=$(realpath "$1")
OUTPUT_FILE=$(realpath "$2")

SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Navigate to the converter directory
cd "$SCRIPT_DIR/rcv-onnx" || { echo "Error: rcv-onnx directory not found next to the script."; exit 1; }

# Automatically install dependencies on the first run
if [ ! -d "node_modules" ]; then
    echo "First run detected. Installing npm dependencies..."
    npm install
fi

# Execute the converter
node convert.js "$INPUT_FILE" "$OUTPUT_FILE"