from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class BaseLLM(ABC, BaseModel):
    """
    Abstract base class for Language Learning Models (LLMs). This class defines the basic structure and methods for LLMs.
    """
    model: str
    # system_prompt: Optional[str] = None

    model_config = {"protected_namespaces":()}

    @abstractmethod
    def _get_chat_completion(
        self,
        messages: List[Dict[str, str]],
    ):
        """
        Abstract method to generate a chat completion based on a list of messages.

        Args:
            messages (List[Dict[str, str]]): A list of messages where each message is a dictionary with keys 'text' and 'role'.
        """

    @abstractmethod
    def invoke(
        self,
        query: str,
        **kwargs
    ) -> str:
        """
        Abstract method to invoke the LLM with a given query.

        Args:
            query (str): The query to invoke the LLM with.

        Returns:
            str: The response from the LLM.
        """