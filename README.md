# Mac Agent (crewAI Edition)

This is an intelligent agent that uses crewAI to translate your natural language requests into executable shell commands on your macOS.

It leverages a Large Language Model (LLM) to understand your intent and uses a dedicated `ShellTool` to execute commands, making it a robust and flexible automation assistant.

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

4.  **Make the Script Executable:**
    You need to give the main script permission to run.
    ```bash
    chmod +x do.sh
    ```

## Usage

To use the agent, simply run the `do.sh` script with your request in plain English, enclosed in quotes.

```bash
./do.sh "your request here"
```

### Examples

```bash
# Find large files in your downloads folder
./do.sh "Find all files larger than 100MB in my downloads folder."

# Control an application using osascript
./do.sh "Tell the Music app to play the next song."

# A more complex, multi-step command
./do.sh "What is the current weather in San Francisco?"
```

## How It Works

1.  You run `./do.sh "your request"`.
2.  The shell script invokes the `crew.py` script.
3.  `crew.py` defines a specialized **Agent** whose goal is to fulfill your request.
4.  It creates a **Task** with your prompt and assigns it to the agent.
5.  The agent uses its **ShellTool** to think, plan, and execute the necessary shell commands.
6.  crewAI's verbose output shows you the agent's thought process, the commands it's running, and the final result.

**Safety:** The agent will show you the commands it intends to run as part of its thought process. **Always monitor the agent's actions**, especially when you ask it to perform tasks that might modify or delete files.
