#!/bin/bash

cd "/Users/eduardo/Documents/GitHub/dont-be-square/diagrams"
mkdir -p .temp views
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

extract_and_compile() {
    local md_file=$1
    local name=$(basename "$md_file" .md)
    
    echo "Processing $name..."
    
    # Extract mermaid code
    awk '/```mermaid/,/```/' "$md_file" | sed '/```mermaid/d' | sed '/```/d' > ".temp/${name}.mmd"
    
    if [ -s ".temp/${name}.mmd" ]; then
        /opt/homebrew/bin/mmdc -i ".temp/${name}.mmd" -o "views/${name}.png" -t neutral -b white -w 2400 -H 1800 2>&1 | grep -v "Generating" || true
        if [ -f "views/${name}.png" ]; then
            echo "  ✓ Created views/${name}.png"
        else
            echo "  ✗ Failed to create ${name}.png"
        fi
    else
        echo "  ✗ No mermaid code found in $md_file"
    fi
}

# Compile each phase
extract_and_compile "phase1_fair_structures_comparison.md"
extract_and_compile "phase2_multi_version_evaluation.md"
extract_and_compile "phase3_multi_assay_evaluation.md"
extract_and_compile "phase4_fair_evaluation_hubmap.md"
extract_and_compile "phase5_metadata_fair_scoring.md"

echo ""
echo "Summary:"
ls -1 views/phase*.png 2>/dev/null | wc -l | xargs echo "Total phase diagrams:"
ls views/phase*.png 2>/dev/null

rm -rf .temp
