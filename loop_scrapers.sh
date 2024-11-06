#!/bin/bash

# Get initial SHA of the HEAD commit
last_sha=$(git rev-parse HEAD)

while true; do
    echo "Running scrapers..."
    ./run_scrapers.sh

    # Get current SHA after running scrapers
    current_sha=$(git rev-parse HEAD)

    # Check if SHA changed
    if [ "$current_sha" != "$last_sha" ]; then
        echo "Changes detected, pushing to remotes..."
        git remote | xargs -L1 git push --all
        # Update the last known SHA
        last_sha=$current_sha
    else
        echo "No changes detected"
    fi

    echo "Sleeping for 10 minutes..."
    sleep 600
done
