import os
import requests
from typing import Dict, List, Optional
from pydantic import PositiveFloat, PositiveInt, model_validator

try:
    from groq import Groq, AsyncGroq
    from groq.types.chat import ChatCompletion
except ImportError as e:
    raise Exception("Failed to import Groq. Please ensure it is installed.")

from src.llm.base import BaseLLM


class GroqLLM(BaseLLM):
    api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    max_retries: PositiveInt = 3

    @model_validator(mode="after")
    def validate_client(cls, values):
        if values.api_key is None:
            raise ValueError("Groq API key is required.")

        try:
            response = requests.get(
                url=f"https://api.groq.com/openai/v1/models/{values.model}",
                headers={"Authorization": f"Bearer {values.api_key}"}
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            response_content = response.json()

            if values.model.lower() != response_content.get("id", "").lower():
                raise ValueError(f"The specified model '{values.model}' was not found.")

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to validate Groq API key and model: {e}")

        return values

    @property
    def client(self) -> Groq:
        return Groq(
            api_key=self.api_key,
            max_retries=self.max_retries
        )

    @property
    def aclient(self) -> AsyncGroq:
        return AsyncGroq(
            api_key=self.api_key,
            max_retries=self.max_retries
        )

    def _get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: PositiveInt = 1024,
        temperature: PositiveFloat = 0.3,
        top_p: PositiveFloat = 0.1,
        stream: bool = False
    ) -> ChatCompletion:
        return self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream
        )

    async def _aget_chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: PositiveInt = 1024,
        temperature: PositiveFloat = 0.3,
        top_p: PositiveFloat = 0.1,
        stream: bool = False
    ) -> ChatCompletion:
        return await self.aclient.chat.completions.create(
            messages=messages,
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream
        )
    
    def invoke(
        self,
        query: str,
        **kwargs
    ) -> str:
        kwargs["messages"] = kwargs.get("messages") or []
        kwargs["messages"].append({"role": "user", "content": query})

        return self._get_chat_completion(
            **kwargs
        ).choices[0].message.content
    
    async def ainvoke(
        self,
        query: str,
        **kwargs
    ) -> str:
        kwargs["messages"] = kwargs.get("message") or []
        kwargs["messages"].append({"role": "user", "content": query})

        return (await self._aget_chat_completion(
            **kwargs
        )).choices[0].message.content
    

if __name__ == "__main__":
    llm = GroqLLM(model="gemma-7b-it")
    print(llm.invoke(
        query="Hi there",
        messages=[{"role": "system", "content": "you are the most intelligent assistant in the world"}]
    ))
