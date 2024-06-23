#!/bin/bash

# Directory containing the JSONL files
INPUT_DIR="output/scrape/"

# Output file
OUTPUT_FILE="output/output.jsonl"

# Remove the output file if it already exists
if [ -f "$OUTPUT_FILE" ]; then
    rm "$OUTPUT_FILE"
fi

# Create the output file if it doesn't exist
if [ ! -f "$OUTPUT_FILE" ]; then
    touch "$OUTPUT_FILE"
fi

# Loop through each .jsonl file in the directory
for file in "$INPUT_DIR"/*.jsonl; 
do
    # Append the contents of each file to the output file
    cat "$file" >> "$OUTPUT_FILE"
    echo >> "$OUTPUT_FILE"  # Add a newline to separate files
done

sed -i '/^\s*$/d' "$OUTPUT_FILE"

echo "All files have been combined into $OUTPUT_FILE"