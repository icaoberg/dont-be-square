#!/bin/bash

# Script to extract mermaid diagrams from markdown files and compile them to images

DIAGRAMS_DIR="/Users/eduardo/Documents/GitHub/dont-be-square/diagrams"
VIEWS_DIR="${DIAGRAMS_DIR}/views"
TEMP_DIR="${DIAGRAMS_DIR}/.temp"

# Create directories
mkdir -p "$VIEWS_DIR"
mkdir -p "$TEMP_DIR"

# Function to extract mermaid code from markdown and compile
compile_diagram() {
    local md_file="$1"
    local base_name=$(basename "$md_file" .md)
    local relative_path=$(echo "$md_file" | sed "s|${DIAGRAMS_DIR}/||" | sed 's|/|_|g' | sed 's|\.md||')
    
    echo "Processing: $md_file"
    
    # Extract mermaid code block (handles both ```mermaid and ``` mermaid formats)
    awk '/^```mermaid$/,/^```$/' "$md_file" | sed '/^```mermaid$/d' | sed '/^```$/d' > "${TEMP_DIR}/${relative_path}.mmd"
    
    # If that didn't work, try alternative format
    if [ ! -s "${TEMP_DIR}/${relative_path}.mmd" ]; then
        awk '/```mermaid/,/```/' "$md_file" | grep -v '```' > "${TEMP_DIR}/${relative_path}.mmd"
    fi
    
    # Check if mermaid code was extracted
    if [ -s "${TEMP_DIR}/${relative_path}.mmd" ]; then
        echo "  Compiling to PNG..."
        # Set Chrome executable path for Puppeteer
        export PUPPETEER_EXECUTABLE_PATH="${DIAGRAMS_DIR}/chrome/mac_arm-131.0.6778.204/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
        # Fallback to system Chrome if available
        if [ ! -f "$PUPPETEER_EXECUTABLE_PATH" ]; then
            export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        fi
        /opt/homebrew/bin/mmdc -i "${TEMP_DIR}/${relative_path}.mmd" -o "${VIEWS_DIR}/${relative_path}.png" -t default -b white -w 2400 -H 1800 2>&1
        
        if [ $? -eq 0 ]; then
            echo "  ✓ Created: ${VIEWS_DIR}/${relative_path}.png"
        else
            echo "  ✗ Failed to compile: ${relative_path}"
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
