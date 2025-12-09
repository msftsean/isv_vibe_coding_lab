"""Azure OpenAI tool wrapper for CivicNav.

Provides async methods for chat completion and embeddings using
Azure OpenAI with DefaultAzureCredential for authentication.
Includes demo mode for testing without Azure resources.
Supports Ollama/Foundry Local for local LLM inference.
"""

import json
import logging
import random
from typing import Any, TYPE_CHECKING

import httpx

from app.config import get_settings

if TYPE_CHECKING:
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import AsyncAzureOpenAI

logger = logging.getLogger(__name__)


class DemoOpenAITool:
    """OpenAI tool for demo mode with OpenAI API and Ollama/Foundry Local support."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._http_client: httpx.AsyncClient | None = None
        self._openai_client: Any | None = None

    @property
    def http_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client for Ollama requests."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=120.0)
        return self._http_client

    @property
    def openai_client(self):
        """Get or create the OpenAI client."""
        if self._openai_client is None and self.settings.openai_api_key:
            from openai import AsyncOpenAI
            self._openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        return self._openai_client

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Generate chat completion using OpenAI, Ollama, or mock responses."""
        user_message = messages[-1].get("content", "") if messages else ""

        # Check if JSON response expected (either explicit or via prompt keywords)
        is_json_request = (
            (response_format and response_format.get("type") == "json_object") or
            "return only valid json" in user_message.lower() or
            "json object" in user_message.lower()
        )

        # Try OpenAI API first if enabled
        if self.settings.use_openai and self.settings.openai_api_key:
            try:
                return await self._openai_chat_completion(messages, temperature, max_tokens, is_json_request)
            except Exception as e:
                logger.warning(f"OpenAI API request failed, falling back: {e}")

        # Try Ollama if enabled
        if self.settings.use_ollama:
            try:
                return await self._ollama_chat_completion(messages, temperature, max_tokens, is_json_request)
            except Exception as e:
                logger.warning(f"Ollama request failed, falling back to mock: {e}")

        # Fallback to mock responses
        logger.info("[DEMO MODE] Generating mock chat completion")
        if is_json_request:
            return self._generate_demo_classification(user_message)
        return self._generate_demo_answer(user_message)

    async def _openai_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
        is_json_request: bool,
    ) -> str:
        """Call OpenAI's chat completions API."""
        logger.info(f"[OPENAI] Chat completion with model {self.settings.openai_model}")

        kwargs: dict[str, Any] = {
            "model": self.settings.openai_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if is_json_request:
            kwargs["response_format"] = {"type": "json_object"}

        response = await self.openai_client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content or ""
        logger.info(f"[OPENAI] Response received: {len(content)} chars")
        return content

    async def _ollama_chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
        is_json_request: bool,
    ) -> str:
        """Call Ollama's OpenAI-compatible chat completions endpoint."""
        logger.info(f"[OLLAMA] Chat completion with model {self.settings.ollama_model}")

        # Build request payload for Ollama's OpenAI-compatible endpoint
        payload = {
            "model": self.settings.ollama_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        # Request JSON format if needed
        if is_json_request:
            payload["format"] = "json"

        url = f"{self.settings.ollama_endpoint}/v1/chat/completions"
        response = await self.http_client.post(url, json=payload)
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        logger.info(f"[OLLAMA] Response received: {len(content)} chars")
        return content

    def _generate_demo_classification(self, prompt: str) -> str:
        """Generate a mock intent classification JSON."""
        prompt_lower = prompt.lower()

        # Detect category from context
        if "trash" in prompt_lower or "garbage" in prompt_lower or "recycling" in prompt_lower:
            category = "schedule"
            entities = [{"type": "service_type", "value": "trash collection", "start_pos": 0, "end_pos": 5}]
        elif "permit" in prompt_lower or "building" in prompt_lower or "license" in prompt_lower:
            category = "permit"
            entities = [{"type": "service_type", "value": "permit", "start_pos": 0, "end_pos": 6}]
        elif "park" in prompt_lower or "event" in prompt_lower or "festival" in prompt_lower:
            category = "event"
            entities = []
        elif "emergency" in prompt_lower or "911" in prompt_lower or "police" in prompt_lower:
            category = "emergency"
            entities = []
        elif "report" in prompt_lower or "pothole" in prompt_lower or "311" in prompt_lower:
            category = "report"
            entities = []
        else:
            category = "general"
            entities = []

        return json.dumps({
            "category": category,
            "confidence": 0.85,
            "entities": entities
        })

    def _generate_demo_answer(self, query: str) -> str:
        """Generate a demo answer based on the query."""
        query_lower = query.lower()

        if "trash" in query_lower or "garbage" in query_lower or "recycling" in query_lower:
            return (
                "🗑️ **[DEMO MODE]** Trash and recycling collection in our city follows a weekly schedule. "
                "Residential trash pickup occurs every Monday, while recycling is collected on Wednesdays. "
                "Please have your bins at the curb by 7:00 AM on collection day. For large item pickup, "
                "you can schedule a special collection through the Public Works department."
            )
        elif "permit" in query_lower or "building" in query_lower:
            return (
                "🏗️ **[DEMO MODE]** To obtain a building permit, you'll need to submit an application "
                "to the Building Department along with your construction plans. The review process "
                "typically takes 2-4 weeks. Fees vary based on project scope. You can apply online "
                "through the city's permit portal or visit City Hall in person."
            )
        elif "park" in query_lower or "recreation" in query_lower:
            return (
                "🌳 **[DEMO MODE]** Our city has 15 public parks open from dawn to dusk daily. "
                "Recreation programs include youth sports leagues, senior fitness classes, and "
                "summer camps. Park permits for events can be obtained through the Parks & Recreation "
                "department with at least 2 weeks advance notice."
            )
        elif "emergency" in query_lower or "911" in query_lower:
            return (
                "🚨 **[DEMO MODE]** For emergencies, always dial 911. For non-emergency police matters, "
                "call the non-emergency line at 555-0123. The city's Emergency Management Office "
                "provides disaster preparedness resources and maintains the emergency alert system."
            )
        else:
            return (
                f"📋 **[DEMO MODE]** Thank you for your question about '{query[:50]}...'. "
                "In demo mode, this would connect to Azure OpenAI to provide accurate answers "
                "based on the city's knowledge base. To enable full functionality, deploy the "
                "Azure resources using `azd up` and configure the environment variables."
            )

    async def create_embedding(self, text: str) -> list[float]:
        """Create mock embedding for demo mode."""
        logger.info("[DEMO MODE] Generating mock embedding")
        # Return a consistent mock embedding
        random.seed(hash(text) % 2**32)
        return [random.uniform(-1, 1) for _ in range(1536)]

    async def check_connection(self) -> bool:
        """Check if OpenAI/Ollama is accessible, or return True for mock mode."""
        if self.settings.use_openai and self.settings.openai_api_key:
            try:
                # Quick test with minimal tokens
                await self._openai_chat_completion(
                    messages=[{"role": "user", "content": "hi"}],
                    temperature=0,
                    max_tokens=1,
                    is_json_request=False,
                )
                logger.info("[OPENAI] Connection check successful")
                return True
            except Exception as e:
                logger.warning(f"[OPENAI] Connection check failed: {e}")
                return False
        if self.settings.use_ollama:
            try:
                url = f"{self.settings.ollama_endpoint}/api/tags"
                response = await self.http_client.get(url)
                response.raise_for_status()
                logger.info("[OLLAMA] Connection check successful")
                return True
            except Exception as e:
                logger.warning(f"[OLLAMA] Connection check failed: {e}")
                return False
        return True  # Mock mode is always "connected"


class OpenAITool:
    """Wrapper for Azure OpenAI operations.

    Uses DefaultAzureCredential for authentication, supporting both
    local development (Azure CLI) and production (managed identity).
    """

    def __init__(self) -> None:
        """Initialize the OpenAI tool with Azure credentials."""
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
        from openai import AsyncAzureOpenAI

        self.settings = get_settings()
        self._client: AsyncAzureOpenAI | None = None
        self._DefaultAzureCredential = DefaultAzureCredential
        self._get_bearer_token_provider = get_bearer_token_provider
        self._AsyncAzureOpenAI = AsyncAzureOpenAI

    @property
    def client(self):
        """Get or create the AsyncAzureOpenAI client."""
        if self._client is None:
            credential = self._DefaultAzureCredential()
            token_provider = self._get_bearer_token_provider(
                credential, "https://cognitiveservices.azure.com/.default"
            )
            self._client = self._AsyncAzureOpenAI(
                azure_endpoint=self.settings.azure_openai_endpoint,
                azure_ad_token_provider=token_provider,
                api_version=self.settings.azure_openai_api_version,
            )
        return self._client

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Generate a chat completion using Azure OpenAI.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            response_format: Optional response format specification

        Returns:
            The assistant's response text
        """
        logger.debug(f"Chat completion with {len(messages)} messages")

        kwargs: dict[str, Any] = {
            "model": self.settings.azure_openai_chat_deployment,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = await self.client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content or ""
        logger.debug(f"Chat completion response: {len(content)} chars")
        return content

    async def create_embedding(self, text: str) -> list[float]:
        """Create an embedding vector for the given text.

        Args:
            text: The text to embed

        Returns:
            List of floats representing the embedding vector
        """
        logger.debug(f"Creating embedding for text: {len(text)} chars")

        response = await self.client.embeddings.create(
            model=self.settings.azure_openai_embedding_deployment,
            input=text,
        )

        embedding = response.data[0].embedding
        logger.debug(f"Created embedding with {len(embedding)} dimensions")
        return embedding

    async def check_connection(self) -> bool:
        """Check if the OpenAI service is accessible.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Simple test with minimal tokens
            await self.chat_completion(
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
            )
            return True
        except Exception as e:
            logger.warning(f"OpenAI connection check failed: {e}")
            return False


# Global instance for convenience
_openai_tool: OpenAITool | DemoOpenAITool | None = None


def get_openai_tool() -> OpenAITool | DemoOpenAITool:
    """Get the global OpenAI tool instance.

    Returns DemoOpenAITool if demo_mode is enabled or Azure is not configured.
    """
    global _openai_tool
    if _openai_tool is None:
        settings = get_settings()
        if settings.demo_mode or not settings.is_configured:
            logger.info("Using DemoOpenAITool (demo mode or Azure not configured)")
            _openai_tool = DemoOpenAITool()
        else:
            _openai_tool = OpenAITool()
    return _openai_tool
