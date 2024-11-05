#!/bin/bash

# Make the script exit on any error
set -e

TOP=$(cd "$(dirname "$0")" && pwd)
cd "${TOP}"

# Function to normalize state name for directory
normalize_state_name() {
    echo "$1" | tr ' ' '_'
}

# Function to check if jurisdiction is fully reported
check_fully_reported() {
    local json_file="$1"
    if [ -f "$json_file" ]; then
        reporting=$(cat "$json_file" | python3 -c "import sys, json; print(json.load(sys.stdin).get('reporting', 0))")
        if [ "$reporting" = "100" ]; then
            return 0  # true in bash
        fi
    fi
    return 1  # false in bash
}

# Array of states
states=(
    "Alabama" "Alaska" "Arizona" "Arkansas" "California" "Colorado" "Connecticut" 
    "Delaware" "District of Columbia" "Florida" "Georgia" "Hawaii" "Idaho" "Illinois" 
    "Indiana" "Iowa" "Kansas" "Kentucky" "Louisiana" "Maine" "Maryland" 
    "Massachusetts" "Michigan" "Minnesota" "Mississippi" "Missouri" "Montana" 
    "Nebraska" "Nevada" "New Hampshire" "New Jersey" "New Mexico" "New York" 
    "North Carolina" "North Dakota" "Ohio" "Oklahoma" "Oregon" "Pennsylvania" 
    "Rhode Island" "South Carolina" "South Dakota" "Tennessee" "Texas" "Utah" 
    "Vermont" "Virginia" "Washington" "West Virginia" "Wisconsin" "Wyoming"
)

# Process each state
for state in "${states[@]}"; do
    state_dir="scrapers/$(normalize_state_name "$state")"
    
    # Create state directory if it doesn't exist
    mkdir -p "$state_dir"
    
    # Initialize latest.json if it doesn't exist
    if [ ! -f "$state_dir/latest.json" ]; then
        echo '{
            "counted": {
                "republican": 0,
                "democrat": 0
            },
            "exit_poll": {
                "republican": 0,
                "democrat": 0
            },
            "reporting": 0,
            "called": false
        }' > "$state_dir/latest.json"
    fi
    
    # Check if scraper exists and jurisdiction isn't fully reported
    if [ -f "$state_dir/scraper.py" ]; then
        if check_fully_reported "$state_dir/latest.json"; then
            echo "Skipping $state - already 100% reported"
            continue
        fi
        
        echo "Running scraper for $state..."
        cd "$state_dir"
        python3 "scraper.py"
        cd "$TOP"
        # If changes were made to latest.json, commit them
        if git diff --quiet "$state_dir/latest.json"; then
            echo "No changes for $state"
        else
            git add "$state_dir/latest.json"
            git commit -m "Update results for $state"
        fi
    fi
done

# Run the assembly script to create the final results
python3 assemble.py

# Commit the assembled results if changed
if ! git diff --quiet current_results.json; then
    git add current_results.json
    git commit -m "Update assembled results"
fi