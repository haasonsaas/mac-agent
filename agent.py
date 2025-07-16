import os
import sys
import json
from openai import OpenAI

def load_config():
    """Loads configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if not os.path.exists(config_path):
        print("echo 'Error: config.json not found. Please copy config.json.default to config.json and fill in your details.'")
        sys.exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

def load_history(config):
    """Loads conversation history from the file specified in config."""
    history_path = os.path.join(os.path.dirname(__file__), config.get("history_file", ".history.json"))
    if not os.path.exists(history_path):
        return []
    with open(history_path, 'r') as f:
        return json.load(f)

def save_history(history, config):
    """Saves conversation history to the file specified in config."""
    history_path = os.path.join(os.path.dirname(__file__), config.get("history_file", ".history.json"))
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)

def generate_script(prompt, history, config):
    """Generates a script using the LLM, considering conversation history."""
    api_key = os.environ.get("OPENAI_API_KEY") or config.get("openai_api_key")
    client = OpenAI(
        api_key=api_key,
        base_url=config.get("openai_base_url")
    )

    system_prompt = {
        "role": "system",
        "content": (
            "You are an expert macOS automation assistant. Your task is to generate a single, executable shell script that accomplishes the user's goal. "
            "The script will be run on macOS, so use appropriate commands. "
            "Prioritize robust shell commands (`find`, `grep`, `curl`, etc.) where possible. "
            "Use `osascript` (AppleScript or JXA) only when necessary to control applications or the GUI. "
            "The output should be ONLY the shell script, with no explanation or markdown formatting. "
            "If you are asked to correct an error, the previous attempt and the error will be in the history. Analyze the error and provide a corrected script. Do not repeat the same mistake."
        )
    }
    messages = [system_prompt] + history + [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model=config.get("model", "gpt-4o"),
            messages=messages,
            temperature=0.2,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"echo 'Error communicating with LLM: {e}'"

if __name__ == "__main__":
    config = load_config()
    history = load_history(config)

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        # Handle self-correction input
        if "--error" in sys.argv:
            error_index = sys.argv.index("--error")
            if error_index + 1 < len(sys.argv):
                error_message = sys.argv[error_index + 1]
                # Add the error context to the history for the LLM
                history.append({"role": "tool", "content": f"The last script failed with this error:\n{error_message}"})

        generated_script = generate_script(user_prompt, history, config)
        # Add the successful prompt and response to history
        history.append({"role": "user", "content": user_prompt})
        history.append({"role": "assistant", "content": generated_script})
        # Trim history to keep it from growing too large
        max_history = config.get("max_history_length", 10)
        if len(history) > max_history * 2: # Each interaction is 2 items
            history = history[-(max_history * 2):]
        save_history(history, config)
        print(generated_script)
    else:
        print("echo 'Error: No prompt provided.'")