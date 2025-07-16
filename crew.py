import os
import sys
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import DuckDuckGoSearchRun
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

# Instantiate tools
shell_tool = ShellTool()
search_tool = DuckDuckGoSearchRun()

# Define the agent
mac_agent = Agent(
    role='Senior macOS Automation and Research Specialist',
    goal='Fulfill user requests by combining web research with local command execution to achieve complex tasks.',
    backstory=(
        "You are an expert in macOS automation and an adept web researcher. You have access to two powerful tools: "
        "a shell for executing local commands and a web search tool for finding information. "
        "Your primary goal is to seamlessly integrate these tools. For example, if a user asks to 'download the latest version of node.js', "
        "you will first use the search tool to find the download URL, and then use the shell tool with `curl` to download it. "
        "You are methodical, breaking down complex problems into a sequence of research and execution steps."
    ),
    tools=[shell_tool, search_tool],
    allow_delegation=False,
    verbose=True
)

# Define the task
def create_task(user_prompt):
    return Task(
        description=f"The user wants to perform the following action: '{user_prompt}'. Your task is to understand the request, create a plan, and then use your available tools (ShellTool and DuckDuckGoSearchRun) to execute the plan. The final answer must be the result of your work.",
        expected_output="A summary of the actions taken and the final result or output.",
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
