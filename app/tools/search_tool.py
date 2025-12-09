"""Azure AI Search tool wrapper for CivicNav.

Provides async methods for hybrid search (vector + keyword + semantic)
using Azure AI Search with DefaultAzureCredential for authentication.
Includes demo mode for testing without Azure resources.
"""

import json
import logging
from pathlib import Path
from typing import Any

from app.config import get_settings
from app.models.schemas import Category, SearchResult

logger = logging.getLogger(__name__)


class DemoSearchTool:
    """Mock Search tool for demo mode using local knowledge base."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._knowledge_base: list[dict] | None = None

    @property
    def knowledge_base(self) -> list[dict]:
        """Load knowledge base from JSON file."""
        if self._knowledge_base is None:
            kb_path = Path(__file__).parent.parent.parent / "data" / "knowledge_base.json"
            if kb_path.exists():
                with open(kb_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Handle both flat array and {entries: [...]} format
                    if isinstance(data, dict) and "entries" in data:
                        self._knowledge_base = data["entries"]
                    elif isinstance(data, list):
                        self._knowledge_base = data
                    else:
                        self._knowledge_base = []
                logger.info(f"[DEMO MODE] Loaded {len(self._knowledge_base)} knowledge base entries")
            else:
                logger.warning(f"[DEMO MODE] Knowledge base not found at {kb_path}")
                self._knowledge_base = []
        return self._knowledge_base

    async def hybrid_search(
        self,
        query: str,
        vector: list[float],
        top_k: int = 5,
        category: Category | None = None,
    ) -> list[SearchResult]:
        """Perform mock hybrid search using local knowledge base."""
        logger.info(f"[DEMO MODE] Hybrid search: '{query}'")
        return await self._search(query, top_k, category)

    async def keyword_search(
        self,
        query: str,
        top_k: int = 5,
        category: Category | None = None,
    ) -> list[SearchResult]:
        """Perform mock keyword search using local knowledge base."""
        logger.info(f"[DEMO MODE] Keyword search: '{query}'")
        return await self._search(query, top_k, category)

    async def _search(
        self,
        query: str,
        top_k: int = 5,
        category: Category | None = None,
    ) -> list[SearchResult]:
        """Simple text-based search on the knowledge base."""
        query_lower = query.lower()
        query_terms = query_lower.split()

        results: list[tuple[float, dict]] = []

        for entry in self.knowledge_base:
            # Filter by category if specified
            if category and entry.get("category") != category.value:
                continue

            # Simple relevance scoring based on term matches
            content = (entry.get("title", "") + " " + entry.get("content", "")).lower()
            score = sum(1.0 for term in query_terms if term in content)

            # Boost score if title contains terms
            title_lower = entry.get("title", "").lower()
            score += sum(0.5 for term in query_terms if term in title_lower)

            if score > 0:
                results.append((score, entry))

        # Sort by score and take top_k
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:top_k]

        search_results: list[SearchResult] = []
        for score, entry in top_results:
            # Create highlight snippet
            content = entry.get("content", "")
            highlight = content[:200] + "..." if len(content) > 200 else content

            search_results.append(
                SearchResult(
                    id=entry.get("id", ""),
                    entry_id=entry.get("id", ""),
                    title=entry.get("title", ""),
                    content=content,
                    category=Category(entry.get("category", "general")),
                    service_type=entry.get("service_type"),
                    department=entry.get("department"),
                    relevance_score=min(score / len(query_terms), 1.0) if query_terms else 0.5,
                    highlight=highlight,
                )
            )

        logger.info(f"[DEMO MODE] Found {len(search_results)} results")
        return search_results

    async def get_categories(self) -> dict[str, int]:
        """Get count of entries per category from local knowledge base."""
        logger.info("[DEMO MODE] Getting category counts")
        category_counts: dict[str, int] = {}
        for entry in self.knowledge_base:
            cat = entry.get("category", "general")
            category_counts[cat] = category_counts.get(cat, 0) + 1
        return category_counts

    async def check_connection(self) -> bool:
        """Demo mode is always 'connected'."""
        return True


class SearchTool:
    """Wrapper for Azure AI Search operations.

    Uses DefaultAzureCredential for authentication and supports
    hybrid search combining vector, keyword, and semantic ranking.
    """

    def __init__(self) -> None:
        """Initialize the Search tool with Azure credentials."""
        from azure.identity import DefaultAzureCredential
        from azure.search.documents import SearchClient
        from azure.search.documents.models import QueryType, VectorizedQuery

        self.settings = get_settings()
        self._client = None
        self._DefaultAzureCredential = DefaultAzureCredential
        self._SearchClient = SearchClient
        self._QueryType = QueryType
        self._VectorizedQuery = VectorizedQuery

    @property
    def client(self):
        """Get or create the SearchClient."""
        if self._client is None:
            credential = self._DefaultAzureCredential()
            self._client = self._SearchClient(
                endpoint=self.settings.azure_search_endpoint,
                index_name=self.settings.azure_search_index,
                credential=credential,
            )
        return self._client

    async def hybrid_search(
        self,
        query: str,
        vector: list[float],
        top_k: int = 5,
        category: Category | None = None,
    ) -> list[SearchResult]:
        """Perform hybrid search combining vector, keyword, and semantic ranking.

        Args:
            query: The search query text
            vector: The embedding vector for vector search
            top_k: Number of results to return
            category: Optional category filter

        Returns:
            List of SearchResult objects sorted by relevance
        """
        logger.debug(f"Hybrid search: '{query}' (top_k={top_k})")

        # Build filter if category specified
        filter_expr = f"category eq '{category.value}'" if category else None

        # Create vector query
        vector_query = self._VectorizedQuery(
            vector=vector,
            k_nearest_neighbors=top_k,
            fields="content_vector",
        )

        # Execute hybrid search with semantic ranking
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            query_type=self._QueryType.SEMANTIC,
            semantic_configuration_name="default",
            top=top_k,
            filter=filter_expr,
            select=["id", "title", "content", "category", "service_type", "department"],
            highlight_fields="content",
        )

        search_results: list[SearchResult] = []
        for result in results:
            # Get highlight if available
            highlights = result.get("@search.highlights", {})
            highlight = highlights.get("content", [""])[0] if highlights else None

            search_results.append(
                SearchResult(
                    id=result["id"],
                    entry_id=result["id"],
                    title=result["title"],
                    content=result["content"],
                    category=Category(result["category"]),
                    service_type=result.get("service_type"),
                    department=result.get("department"),
                    relevance_score=result.get("@search.score", 0.0),
                    highlight=highlight,
                )
            )

        logger.debug(f"Found {len(search_results)} results")
        return search_results

    async def keyword_search(
        self,
        query: str,
        top_k: int = 5,
        category: Category | None = None,
    ) -> list[SearchResult]:
        """Perform keyword-only search.

        Args:
            query: The search query text
            top_k: Number of results to return
            category: Optional category filter

        Returns:
            List of SearchResult objects sorted by relevance
        """
        logger.debug(f"Keyword search: '{query}' (top_k={top_k})")

        filter_expr = f"category eq '{category.value}'" if category else None

        results = self.client.search(
            search_text=query,
            top=top_k,
            filter=filter_expr,
            select=["id", "title", "content", "category", "service_type", "department"],
            highlight_fields="content",
        )

        search_results: list[SearchResult] = []
        for result in results:
            highlights = result.get("@search.highlights", {})
            highlight = highlights.get("content", [""])[0] if highlights else None

            search_results.append(
                SearchResult(
                    id=result["id"],
                    entry_id=result["id"],
                    title=result["title"],
                    content=result["content"],
                    category=Category(result["category"]),
                    service_type=result.get("service_type"),
                    department=result.get("department"),
                    relevance_score=result.get("@search.score", 0.0),
                    highlight=highlight,
                )
            )

        return search_results

    async def get_categories(self) -> dict[str, int]:
        """Get count of entries per category.

        Returns:
            Dict mapping category name to entry count
        """
        logger.debug("Getting category counts")

        # Use faceting to get category counts
        results = self.client.search(
            search_text="*",
            top=0,
            facets=["category"],
        )

        # Extract facet counts
        category_counts: dict[str, int] = {}
        facets = results.get_facets()
        if facets and "category" in facets:
            for facet in facets["category"]:
                category_counts[facet["value"]] = facet["count"]

        return category_counts

    async def check_connection(self) -> bool:
        """Check if the Search service is accessible.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Simple test search
            list(self.client.search(search_text="*", top=1))
            return True
        except Exception as e:
            logger.warning(f"Search connection check failed: {e}")
            return False


# Global instance for convenience
_search_tool: SearchTool | DemoSearchTool | None = None


def get_search_tool() -> SearchTool | DemoSearchTool:
    """Get the global Search tool instance.

    Returns DemoSearchTool if demo_mode is enabled or Azure is not configured.
    """
    global _search_tool
    if _search_tool is None:
        settings = get_settings()
        if settings.demo_mode or not settings.is_configured:
            logger.info("Using DemoSearchTool (demo mode or Azure not configured)")
            _search_tool = DemoSearchTool()
        else:
            _search_tool = SearchTool()
    return _search_tool
