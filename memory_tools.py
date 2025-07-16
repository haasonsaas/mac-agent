import os
import chromadb
from crewai_tools import BaseTool

class MemoryTool(BaseTool):
    name: str = "Memory Tool"
    description: str = "A tool for storing and retrieving information from long-term memory. Use it to remember facts, preferences, or past interactions."

    def __init__(self, persist_directory: str = "./chroma_db"):
        super().__init__()
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="mac_agent_memory")

    def _run(self, operation: str, query: str = None, document: str = None) -> str:
        """Performs a memory operation.

        Args:
            operation (str): The operation to perform. One of 'store' or 'retrieve'.
            query (str, optional): The query to retrieve information. Required for 'retrieve' operations.
            document (str, optional): The document to store. Required for 'store' operations.
        """
        try:
            if operation == 'store':
                if document is None:
                    return "Error: Document must be provided for a store operation."
                # Generate a unique ID for the document
                doc_id = f"doc_{self.collection.count() + 1}"
                self.collection.add(documents=[document], ids=[doc_id])
                return f"Successfully stored document with ID: {doc_id}."
            
            elif operation == 'retrieve':
                if query is None:
                    return "Error: Query must be provided for a retrieve operation."
                results = self.collection.query(query_texts=[query], n_results=1)
                if results['documents'] and results['documents'][0]:
                    return f"Retrieved: {results['documents'][0][0]}"
                else:
                    return "No relevant information found in memory."
            
            else:
                return f"Error: Invalid operation '{operation}'. Must be one of 'store' or 'retrieve'."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
