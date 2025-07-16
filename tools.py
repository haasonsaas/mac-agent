import os
import subprocess
import sys
from crewai_tools import BaseTool

class ShellTool(BaseTool):
    name: str = "Execute Shell Command"
    description: str = "Executes a shell command and returns the output. Use this for any terminal operations, including file system access, running scripts, or using `osascript`."

    def _run(self, command: str) -> str:
        """Executes the given shell command after user confirmation."""
        
        # Non-interactive mode for tests
        if os.environ.get("MAC_AGENT_NON_INTERACTIVE") == "true":
            print(f"Executing command (non-interactive): {command}")
        else:
            print(f"\nProposed command to execute:")
            print(f"\033[0;33m{command}\033[0m") # Print command in yellow
            
            try:
                # Check if stdin is a TTY. If not, we can't ask for input.
                if not sys.stdin.isatty():
                     print("Non-interactive environment detected. Aborting command execution for safety.")
                     return "Error: Cannot ask for confirmation in a non-interactive environment. Command aborted."

                reply = input("👉 Proceed with execution? (y/n): ").lower().strip()
                if reply != 'y':
                    return "User aborted the command execution."
            except (EOFError, KeyboardInterrupt):
                return "User aborted the command execution."

        try:
            process = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            return process.stdout
        except subprocess.CalledProcessError as e:
            return f"Command failed with exit code {e.returncode}.\nStdout:\n{e.stdout}\nStderr:\n{e.stderr}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

