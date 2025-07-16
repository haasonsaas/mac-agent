#!/bin/bash

# A simple test suite for the mac-agent

# Set non-interactive mode for tests
export MAC_AGENT_NON_INTERACTIVE="true"

# Get the directory of the script itself
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Function to run a test case
run_test() {
    local prompt="$1"
    local expected_output="$2"
    echo -e "\n--- Running Test: '$prompt' ---"
    # Run the agent and capture the output
    # We use a timeout to prevent tests from running indefinitely
    output=$(timeout 30s "$SCRIPT_DIR/do.sh" "$prompt")
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo -e "\033[0;31m❌ Test Failed (Timeout or Error)\033[0m"
        return 1
    fi
    # Check if the output contains the expected string
    if echo "$output" | grep -q "$expected_output"; then
        echo -e "\033[0;32m✅ Test Passed\033[0m"
        return 0
    else
        echo -e "\033[0;31m❌ Test Failed\033[0m"
        echo "Expected to find: '$expected_output'"
        echo "Got: '$output'"
        return 1
    fi
}

# --- Test Cases ---

# Test 1: Simple shell command
run_test "What is the current date?" "$(date +%Y)" # Check for the current year

# Test 2: Web search query
run_test "What is the capital of France?" "Paris"

# Test 3: A more complex task involving planning
run_test "Create a file named 'test_file_tool.txt' with the content 'hello file tool' and then read its content." "Successfully wrote to test_file_tool.txt." "hello file tool"

# Test 4: AppleScriptTool usage (display notification)
run_test "Display a notification saying 'Hello from Mac Agent!'" "Hello from Mac Agent!"

# Clean up the test files
rm test.txt test_file_tool.txt 2>/dev/null

echo -e "\n--- Test Suite Finished ---"
