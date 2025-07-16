import os
from crewai_tools import BaseTool
from typing import List

class FileTool(BaseTool):
    name: str = "File System Tool"
    description: str = "A tool for interacting with the file system. Use it to read, write, and list files."

    def _run(self, operation: str, path: str, content: str = None) -> str:
        """Performs a file system operation.

        Args:
            operation (str): The operation to perform. One of 'read', 'write', or 'list'.
            path (str): The path to the file or directory.
            content (str, optional): The content to write to the file. Required for 'write' operations.
        """
        try:
            if operation == 'write':
                if content is None:
                    return "Error: Content must be provided for a write operation."
                with open(path, 'w') as f:
                    f.write(content)
                return f"Successfully wrote to {path}."
            
            elif operation == 'read':
                with open(path, 'r') as f:
                    return f.read()
            
            elif operation == 'list':
                if not os.path.isdir(path):
                    return f"Error: {path} is not a valid directory."
                return "\n".join(os.listdir(path))
            
            else:
                return f"Error: Invalid operation '{operation}'. Must be one of 'read', 'write', or 'list'."
        except FileNotFoundError:
            return f"Error: The path {path} was not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

