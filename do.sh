#!/bin/bash

# Check if a prompt was provided
if [ -z "$1" ]; then
    echo "Usage: ./do.sh \"Your request in plain English\""
    exit 1
fi

# Get the directory of the script itself
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# The user's prompt
PROMPT="$1"

# Run the crewAI agent
python3 "$SCRIPT_DIR/crew.py" "$PROMPT"

