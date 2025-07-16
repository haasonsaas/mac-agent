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

# Call the Python agent to generate the script
# The output of this command will be the generated shell script
echo "🤖 Thinking..."
GENERATED_SCRIPT=$(python3 "$SCRIPT_DIR/agent.py" "$PROMPT")

# --- Safety Check ---
# Display the generated script to the user and ask for confirmation

echo -e "\n--------------------------------------------------"
echo -e "Proposed script to execute:
"
echo -e "\033[0;33m$GENERATED_SCRIPT\033[0m" # Print script in yellow
echo -e "\n--------------------------------------------------"

read -p "👉 Proceed with execution? (y/n): " -n 1 -r
echo # Move to a new line

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n🚀 Executing..."
    # Execute the script
    eval "$GENERATED_SCRIPT"
    echo -e "\n✅ Done."
else
    echo -e "\n🚫 Aborted."
fi
