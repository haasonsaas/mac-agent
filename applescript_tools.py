import subprocess
from crewai_tools import BaseTool

class AppleScriptTool(BaseTool):
    name: str = "AppleScript Execution Tool"
    description: str = "Executes AppleScript or JavaScript for Automation (JXA) code. Use this tool to control macOS applications, display notifications, or interact with the GUI."

    def _run(self, script_code: str, language: str = "AppleScript") -> str:
        """Executes the given AppleScript or JXA code.

        Args:
            script_code (str): The AppleScript or JXA code to execute.
            language (str, optional): The language of the script. Can be 'AppleScript' or 'JavaScript'. Defaults to 'AppleScript'.
        """
        try:
            if language.lower() == "applescript":
                cmd = ["osascript", "-e", script_code]
            elif language.lower() == "javascript":
                cmd = ["osascript", "-l", "JavaScript", "-e", script_code]
            else:
                return f"Error: Invalid language '{language}'. Must be 'AppleScript' or 'JavaScript'."

            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return process.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"AppleScript execution failed with error: {e.stderr.strip()}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
