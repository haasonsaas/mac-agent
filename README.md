# Mac Agent

This is a simple agent that uses a Large Language Model (LLM) to translate your natural language requests into executable shell commands on your macOS.

It is designed to be a "hybrid tool-using agent," meaning it will try to use the best tool for the job, whether that's a standard shell command (`find`, `curl`) or `osascript` for controlling applications and the GUI.

## Setup

1.  **Install Python:**
    Make sure you have Python 3 installed on your system.

2.  **Install Dependencies:**
    This agent uses the `openai` library to communicate with the LLM. You'll need to install it.
    ```bash
    pip install openai
    ```

3.  **Set Your API Key:**
    The agent needs an API key for an LLM provider (like OpenAI, Anthropic, or a local model provider). You must set this as an environment variable. Add the following line to your shell's configuration file (`~/.zshrc`, `~/.bashrc`, etc.).

    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```
    *Note: Although the variable is `OPENAI_API_key`, you can use it with any service that has an OpenAI-compatible API, including local models run with `ollama` or `lm-studio` by also setting the `OPENAI_BASE_URL`.*

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
# Example 1: Using shell commands
./do.sh "Find all files larger than 10MB in my downloads folder and list them."

# Example 2: Using osascript to control an app
./do.sh "Tell Spotify to play the next track."

# Example 3: A hybrid approach
./do.sh "Take a screenshot, save it to my desktop with the name 'test.png', and then open it."
```

## How It Works

1.  You run `./do.sh "your request"`.
2.  The shell script passes your request to the `agent.py` Python script.
3.  The Python script constructs a detailed prompt, asking the LLM to generate a shell script to accomplish your goal.
4.  The LLM returns a shell script.
5.  The agent shows you the proposed script and asks for your confirmation.
6.  If you type `y` and press Enter, the script is executed. Otherwise, it is aborted.

**Safety:** The confirmation step is a critical safety feature. **Always review the script before you approve it**, especially if it includes commands that modify or delete files (`mv`, `rm`, etc.).
