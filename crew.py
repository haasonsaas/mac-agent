import os
import sys
import json
from crewai import Agent, Task, Crew, Process
from crewai_tools import DuckDuckGoSearchRun
from tools import ShellTool
from file_tools import FileTool

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
file_tool = FileTool()

# --- Define Agents ---

planner = Agent(
    role="Senior Planner and Research Analyst",
    goal="Analyze user requests, break them down into a clear, step-by-step plan, and conduct web research for any required information.",
    backstory=(
        "You are a meticulous planner. Your expertise lies in taking a complex user goal and decomposing it into a series of simple, actionable steps. "
        "You use your web search tool to gather all necessary information, such as URLs, commands, or best practices, before creating the final plan. "
        "Your plans are passed to an Executor agent, so they must be unambiguous and easy to follow."
    ),
    tools=[search_tool],
    allow_delegation=False,
    verbose=True
)

executor = Agent(
    role="Command and File Execution Specialist",
    goal="Execute the shell commands and file operations outlined in a given plan with precision and care.",
    backstory=(
        "You are an expert at executing tasks. You take a step-by-step plan and use the best tool for the job. "
        "For general shell commands, use the ShellTool. "
        "For file system operations like reading, writing, or listing files, **you must use the FileTool** as it is safer and more structured. "
        "You do not deviate from the plan. You are careful and will report the results of each action accurately."
    ),
    tools=[shell_tool, file_tool],
    allow_delegation=False,
    verbose=True
)

# --- Define Tasks ---

def create_tasks(user_prompt):
    planning_task = Task(
        description=f"The user wants to: '{user_prompt}'. Analyze this request and create a detailed, step-by-step plan to achieve the goal. If you need information, use your search tool. The final output of this task must be the plan.",
        expected_output="A numbered, step-by-step plan that the Executor agent can follow.",
        agent=planner
    )

    execution_task = Task(
        description=(
            "Take the plan provided and execute each step using the most appropriate tool. "
            "Use the FileTool for reading, writing, and listing files. Use the ShellTool for all other terminal commands. "
            "The final answer must be a summary of the results of each step."
        ),
        expected_output="A summary of the execution results for each step in the plan.",
        agent=executor,
        context=[planning_task] # This task depends on the output of the planning_task
    )
    return [planning_task, execution_task]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
        tasks = create_tasks(user_prompt)
        crew = Crew(
            agents=[planner, executor],
            tasks=tasks,
            process=Process.sequential,
            verbose=2
        )
        result = crew.kickoff()
        print("\n--- Task Result ---")
        print(result)
    else:
        print("Error: No prompt provided.")