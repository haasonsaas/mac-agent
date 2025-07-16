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

def generate_script(prompt, config):
    """Generates a script using the LLM based on the user's prompt."""
    api_key = os.environ.get("OPENAI_API_KEY") or config.get("openai_api_key")
    
    client = OpenAI(
        api_key=api_key,
        base_url=config.get("openai_base_url")
    )

    try:
        response = client.chat.completions.create(
            model=config.get("model", "gpt-4o"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert macOS automation assistant. Your task is to generate a single, executable shell script that accomplishes the user's goal. "
                        "The script will be run on macOS, so use appropriate commands. "
                        "Prioritize robust shell commands (`find`, `grep`, `curl`, etc.) where possible. "
                        "Use `osascript` (AppleScript or JXA) only when necessary to control applications or the GUI. "
                        "The output should be ONLY the shell script, with no explanation or markdown formatting. "
                        "Ensure the script is safe and does not perform destructive actions without clear intent from the user's prompt."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"echo 'Error communicating with LLM: {e}'"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        config = load_config()
        generated_script = generate_script(user_prompt, config)
        print(generated_script)
    else:
        print("echo 'Error: No prompt provided.'")
