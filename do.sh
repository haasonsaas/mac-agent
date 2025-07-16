#!/bin/bash

# Check if a prompt was provided
if [ -z "$1" ]; then
    echo "Usage: ./do.sh \"Your request in plain English\""
    exit 1
fi

# Get the directory of the script itself
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# The user's initial prompt
PROMPT="$1"
ERROR_MESSAGE=""
ATTEMPT=1

while true; do
    # On the first attempt, just say "Thinking". On subsequent attempts, say "Attempting a fix..."
    if [ $ATTEMPT -eq 1 ]; then
        echo "🤖 Thinking..."
    else
        echo "🤖 Attempting a fix..."
    fi

    # Construct the command to call the Python agent
    AGENT_CMD="python3 \"$SCRIPT_DIR/agent.py\" \"$PROMPT\""
    if [ -n "$ERROR_MESSAGE" ]; then
        AGENT_CMD="$AGENT_CMD --error \"$ERROR_MESSAGE\""
    fi

    # Generate the script
    GENERATED_SCRIPT=$(eval "$AGENT_CMD")

    # --- Safety Check ---
    echo -e "\n--------------------------------------------------"
    if [ $ATTEMPT -gt 1 ]; then
        echo -e "Proposed fix (Attempt #$ATTEMPT):\n"
    else
        echo -e "Proposed script to execute:\n"
    fi
    echo -e "\033[0;33m$GENERATED_SCRIPT\033[0m" # Print script in yellow
    echo -e "--------------------------------------------------"

    read -p "👉 Proceed with execution? (y/n): " -n 1 -r
    echo # Move to a new line

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "\n🚀 Executing..."
        # Execute the script, capturing stderr to a variable
        # We use a temporary file to robustly capture stderr, even with complex scripts
        ERROR_OUTPUT=$(mktemp)
        eval "$GENERATED_SCRIPT" 2> "$ERROR_OUTPUT"
        EXIT_CODE=$?
        
        # Read the error from the temp file
        ERROR_MESSAGE=$(<"$ERROR_OUTPUT")
        rm "$ERROR_OUTPUT"

        if [ $EXIT_CODE -eq 0 ]; then
            echo -e "\n✅ Done."
            break # Exit the loop on success
        else
            echo -e "\n❌ Script failed with exit code $EXIT_CODE."
            if [ -n "$ERROR_MESSAGE" ]; then
                echo -e "Error details:\n\033[0;31m$ERROR_MESSAGE\033[0m" # Print error in red
            fi
            
            read -p "👉 Would you like to attempt a correction? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                ATTEMPT=$((ATTEMPT + 1))
                # The loop will continue with the captured ERROR_MESSAGE
            else
                echo -e "\n🚫 Aborted."
                break # Exit loop if user doesn't want to correct
            fi
        fi
    else
        echo -e "\n🚫 Aborted."
        break # Exit loop if user aborts execution
    fi
done