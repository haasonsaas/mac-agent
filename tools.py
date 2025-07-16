import os
import subprocess
from crewai_tools import BaseTool

class ShellTool(BaseTool):
    name: str = "Execute Shell Command"
    description: str = "Executes a shell command and returns the output. Use this for any terminal operations, including file system access, running scripts, or using `osascript`."

    def _run(self, command: str) -> str:
        """Executes the given shell command."""
        print(f"\nExecuting command: {command}\n")
        try:
            # We use a temporary file to robustly capture stderr, even with complex scripts
            error_output = os.path.join(os.path.dirname(__file__), ".error_output.tmp")
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

