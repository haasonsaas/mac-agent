import os
import sys
import json
from crewai import Agent, Task, Crew, Process
from tools import ShellTool

def load_config():
    """Loads configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if not os.path.exists(config_path):
        print("Error: config.json not found. Please copy config.json.default to config.json and fill in your details.")
        sys.exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

# Load configuration
config = load_config()
api_key = os.environ.get("OPENAI_API_KEY") or config.get("openai_api_key")

# Set up the OpenAI client
os.environ["OPENAI_API_KEY"] = api_key
if config.get("openai_base_url"):
    os.environ["OPENAI_API_BASE"] = config.get("openai_base_url")

# Define the agent
mac_agent = Agent(
    role='macOS Automation Specialist',
    goal='Fulfill user requests by generating and executing shell commands on a macOS system.',
    backstory=(
        "You are an expert in macOS automation. You have access to a shell tool that can execute any command. "
        "Your primary goal is to understand the user's request, formulate a precise shell command to achieve it, and then execute that command. "
        "You should prioritize using standard shell commands (`ls`, `grep`, `find`, etc.) and use `osascript` only when necessary for GUI or application-specific control. "
        "You are methodical and always confirm your actions before executing them."
    ),
    tools=[ShellTool()],
    allow_delegation=False,
    verbose=True
)

# Define the task
def create_task(user_prompt):
    return Task(
        description=f"The user wants to perform the following action: '{user_prompt}'. Your task is to generate the appropriate shell command and execute it using the ShellTool. The final answer must be the output of the shell command.",
        expected_output="The result of the shell command execution.",
        agent=mac_agent
    )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        task = create_task(user_prompt)
        
        crew = Crew(
            agents=[mac_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff()
        
        print("\n--- Task Result ---")
        print(result)
    else:
        print("Error: No prompt provided.")
