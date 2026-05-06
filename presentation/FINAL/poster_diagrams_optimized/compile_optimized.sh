#!/bin/bash

# Script to compile optimized poster diagrams to high-resolution PNG images

DIAGRAMS_DIR="/Users/eduardo/Documents/GitHub/dont-be-square/presentation/FINAL/poster_diagrams_optimized"
VIEWS_DIR="${DIAGRAMS_DIR}/views"
TEMP_DIR="${DIAGRAMS_DIR}/.temp"

# Create directories
mkdir -p "$VIEWS_DIR"
mkdir -p "$TEMP_DIR"

# Function to extract mermaid code from markdown and compile
compile_diagram() {
    local md_file="$1"
    local base_name=$(basename "$md_file" .md)
    local dir_name=$(dirname "$md_file" | xargs basename)
    local output_name="${dir_name}_${base_name}"
    
    echo "Processing: $md_file"
    
    # Extract mermaid code block
    awk '/^```mermaid$/,/^```$/' "$md_file" | sed '/^```mermaid$/d' | sed '/^```$/d' > "${TEMP_DIR}/${output_name}.mmd"
    
    # If that didn't work, try alternative format
    if [ ! -s "${TEMP_DIR}/${output_name}.mmd" ]; then
        awk '/```mermaid/,/```/' "$md_file" | grep -v '```' > "${TEMP_DIR}/${output_name}.mmd"
    fi
    
    # Check if mermaid code was extracted
    if [ -s "${TEMP_DIR}/${output_name}.mmd" ]; then
        echo "  Compiling to PNG (7200x5400)..."
        # Set Chrome executable path for Puppeteer
        export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # Try alternative path if needed
        if [ ! -f "$PUPPETEER_EXECUTABLE_PATH" ]; then
            export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
        fi
        
        /opt/homebrew/bin/mmdc -i "${TEMP_DIR}/${output_name}.mmd" -o "${VIEWS_DIR}/${output_name}.png" -t neutral -b white -w 7200 -H 5400 2>&1
        
        if [ $? -eq 0 ]; then
            echo "  ✓ Created: ${VIEWS_DIR}/${output_name}.png"
        else
            echo "  ✗ Failed to compile: ${output_name}"
        fi
    else
        echo "  ⚠ No mermaid code found in: $md_file"
    fi
}

# Find all markdown files and process them
find "$DIAGRAMS_DIR" -name "*.md" -type f | while read -r file; do
    compile_diagram "$file"
done

# Cleanup temp directory
rm -rf "$TEMP_DIR"

echo ""
echo "Compilation complete! Images saved to: $VIEWS_DIR"
