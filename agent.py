import os
import sys
from openai import OpenAI

def generate_script(prompt):
    client = OpenAI()

    # You can swap the model for a different one (e.g., a local model)
    # For local models, you might need to set the base_url:
    # client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or another powerful model like gpt-4, claude-3-opus-20240229
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
        generated_script = generate_script(user_prompt)
        print(generated_script)
    else:
        print("echo 'Error: No prompt provided.'")
