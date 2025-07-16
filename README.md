# Mac Agent (crewAI Multi-Agent Edition)

This is an intelligent agent that uses a multi-agent crewAI system to translate your natural language requests into executable shell commands on your macOS.

It leverages a Large Language Model (LLM) to understand your intent, create a plan, and execute it, making it a robust and flexible automation assistant.

## Architecture

This agent uses a two-agent crew:

1.  **Planner Agent**: Analyzes your request and creates a step-by-step plan. It can use a web search tool to find information.
2.  **Executor Agent**: Takes the plan from the Planner and executes each step using its specialized tools:
    *   **ShellTool**: For general terminal commands.
    *   **FileTool**: For safer reading, writing, and listing of files.
    *   **AppleScriptTool**: For controlling macOS applications and the GUI.
    *   **MemoryTool**: For storing and retrieving information from long-term memory.

This separation of concerns makes the agent more reliable and capable of handling complex, multi-step tasks.

## Human-in-the-Loop: Your Safety is Key

Before the agent executes **any** shell command, it will first print the command and ask for your explicit approval.

```
Proposed command to execute:
[0;33mls -l[0m
👉 Proceed with execution? (y/n):
```

You must type `y` and press Enter for the command to run. This is a critical safety feature to ensure you are always in control of what the agent does on your system.

## Setup

1.  **Install Python:**
    Make sure you have Python 3 installed on your system.

2.  **Install Dependencies:**
    This project uses `pip` to manage dependencies. Install them from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the Agent:**
    Copy the default configuration file to create your own personal config.
    ```bash
    cp config.json.default config.json
    ```
    Now, edit `config.json` and add your LLM API key. You can also change the model and other settings here.

4.  **Make Scripts Executable:**
    You need to give the main scripts permission to run.
    ```bash
    chmod +x do.sh
    chmod +x run_tests.sh
    ```

## Usage

To use the agent, simply run the `do.sh` script with your request in plain English, enclosed in quotes.

```bash
./do.sh "your request here"
```

### Examples

```bash
# A simple command
./do.sh "What day is it today?"

# A command requiring web search
./do.sh "What is the most popular programming language in 2024?"

# A complex, multi-step command
./do.sh "Find the current weather in London, create a file named weather.txt with the information, and then print the file's content."

# Using the AppleScriptTool to display a notification
./do.sh "Display a notification saying 'Hello from your Mac Agent!'"

# Using the MemoryTool to store and retrieve information
./do.sh "Remember that my favorite programming language is Python."
./do.sh "What is my favorite programming language?"
```

## Testing

To ensure the agent is working correctly, you can run the test suite:

```bash
./run_tests.sh
```

This will execute a series of predefined prompts in a non-interactive mode and check if the agent produces the expected output.