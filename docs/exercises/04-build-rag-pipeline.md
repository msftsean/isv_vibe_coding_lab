# 🔍 Exercise 4: Build RAG Pipeline

> ⏱️ **Duration**: 45 minutes | 🎯 **Difficulty**: ⭐⭐ Intermediate | 📋 **Prerequisites**: Exercise 0-3 Complete

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-implementation-red) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 🔧 Understand the search tool implementation | ⬜ |
| 2 | 🔍 Learn how hybrid search works in practice | ⬜ |
| 3 | 📝 Understand the RetrieveAgent implementation | ⬜ |
| 4 | 🧪 Test search with sample queries | ⬜ |
| 5 | 📊 Analyze search results and relevance scores | ⬜ |

---

## 📖 Part 1: Understanding the Search Tool

### 1.1 The Search Tool Architecture

The search tool supports two modes:

```
┌─────────────────────────────────────────────────────────────────┐
│                   🔎 Search Tool Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     get_search_tool()                       ││
│  │                           │                                  ││
│  │        ┌──────────────────┴──────────────────┐              ││
│  │        │                                      │              ││
│  │        ▼                                      ▼              ││
│  │  ┌──────────────┐                   ┌──────────────┐        ││
│  │  │ DemoSearchTool│                   │  SearchTool  │        ││
│  │  │ (Local JSON)  │                   │ (Azure AI)   │        ││
│  │  │               │                   │              │        ││
│  │  │ • Simple text │                   │ • Vector     │        ││
│  │  │   matching    │                   │ • Keyword    │        ││
│  │  │ • No vectors  │                   │ • Semantic   │        ││
│  │  └──────────────┘                   └──────────────┘        ││
│  │        ↑                                      ↑              ││
│  │   demo_mode=True                      Azure configured       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Open the Search Tool File

Open `app/tools/search_tool.py` and find the `DemoSearchTool` class.

### 1.3 Key Methods to Understand

| Method | Purpose | Input | Output |
|--------|---------|-------|--------|
| `hybrid_search()` | Main search method | query, vector, top_k, category | `list[SearchResult]` |
| `keyword_search()` | Keyword-only search | query, top_k, category | `list[SearchResult]` |
| `_search()` | Internal search logic | query, top_k, category | `list[SearchResult]` |
| `get_categories()` | Get category counts | - | `dict[str, int]` |

### 1.4 Understand the Search Algorithm

Look at the `_search()` method in `DemoSearchTool`:

```python
async def _search(
    self,
    query: str,
    top_k: int = 5,
    category: Category | None = None,
) -> list[SearchResult]:
    """Simple text-based search on the knowledge base."""
    query_lower = query.lower()
    query_terms = query_lower.split()  # Split into individual words

    results: list[tuple[float, dict]] = []

    for entry in self.knowledge_base:
        # Filter by category if specified
        if category and entry.get("category") != category.value:
            continue

        # Calculate relevance score
        content = (entry.get("title", "") + " " + entry.get("content", "")).lower()
        score = sum(1.0 for term in query_terms if term in content)

        # Boost score for title matches
        title_lower = entry.get("title", "").lower()
        score += sum(0.5 for term in query_terms if term in title_lower)

        if score > 0:
            results.append((score, entry))

    # Sort by score (highest first) and return top_k
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_k]
```

**How it works:**
1. Split query into words: "trash pickup" → ["trash", "pickup"]
2. For each document, count matching words
3. Add bonus points for title matches
4. Sort by score and return top results

---

## 📖 Part 2: Exploring the Knowledge Base

### 2.1 Open the Knowledge Base

Open `data/knowledge_base.json` and examine the structure:

```json
{
  "entries": [
    {
      "id": "kb-001",
      "title": "Residential Trash Collection Schedule",
      "content": "Residential trash collection occurs every Monday and Thursday...",
      "category": "schedule",
      "service_type": "trash",
      "department": "Public Works"
    },
    // ... more entries
  ]
}
```

### 2.2 Count Entries by Category

Use the API to see category distribution:

```bash
curl http://localhost:8000/api/categories
```

**✅ Expected Output:**
```json
{
  "categories": [
    {"name": "schedule", "count": 4},
    {"name": "permit", "count": 3},
    {"name": "emergency", "count": 2},
    {"name": "report", "count": 7},
    {"name": "event", "count": 4},
    {"name": "general", "count": 6}
  ]
}
```

### 2.3 Examine Sample Entries

Look at a few entries to understand the data:

| ID | Title | Category | Purpose |
|----|-------|----------|---------|
| kb-001 | Residential Trash Collection Schedule | schedule | Trash pickup times |
| kb-003 | Building Permit Application Process | permit | How to get permits |
| kb-005 | Emergency Services - 911 | emergency | Emergency info |
| kb-010 | Report a Pothole | report | Issue reporting |

---

## 📖 Part 3: Understanding the RetrieveAgent

### 3.1 Open the RetrieveAgent

Open `app/agents/retrieve_agent.py` and examine it.

### 3.2 Key Components

```python
class RetrieveAgent(BaseAgent[IntentClassification, list[SearchResult]]):
    """Agent for retrieving relevant documents from the knowledge base."""

    def __init__(self) -> None:
        super().__init__("RetrieveAgent")
        self.search_tool = get_search_tool()
        self.openai_tool = get_openai_tool()

    async def run(self, input_data: IntentClassification) -> AgentResult:
        # 1. Extract the original query
        query = input_data.original_query

        # 2. Create embedding (vector) for semantic search
        embedding = await self.openai_tool.create_embedding(query)

        # 3. Perform hybrid search with category filter
        results = await self.search_tool.hybrid_search(
            query=query,
            vector=embedding,
            top_k=self.settings.search_top_k,
            category=input_data.category if input_data.confidence > 0.7 else None,
        )

        # 4. Return results wrapped in AgentResult
        return AgentResult(output=results, reasoning="...", tools_used=...)
```

### 3.3 Data Flow Through RetrieveAgent

```
┌─────────────────────────────────────────────────────────────────┐
│              📚 RetrieveAgent Data Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: IntentClassification                                    │
│  ┌─────────────────────────────────────────┐                    │
│  │ category: "schedule"                     │                    │
│  │ confidence: 0.95                         │                    │
│  │ original_query: "When is trash pickup?" │                    │
│  └─────────────────────────────────────────┘                    │
│                    │                                             │
│                    ▼                                             │
│  ┌─────────────────────────────────────────┐                    │
│  │ 1️⃣ Create Embedding                      │                    │
│  │    "When is trash pickup?"               │                    │
│  │         ↓                                │                    │
│  │    [0.023, -0.156, 0.891, ...]          │                    │
│  └─────────────────────────────────────────┘                    │
│                    │                                             │
│                    ▼                                             │
│  ┌─────────────────────────────────────────┐                    │
│  │ 2️⃣ Hybrid Search                         │                    │
│  │    • Query text: keyword matching        │                    │
│  │    • Embedding: vector similarity        │                    │
│  │    • Filter: category="schedule"         │                    │
│  └─────────────────────────────────────────┘                    │
│                    │                                             │
│                    ▼                                             │
│  Output: list[SearchResult]                                     │
│  ┌─────────────────────────────────────────┐                    │
│  │ [                                        │                    │
│  │   {title: "Trash Schedule", score: 0.95},│                    │
│  │   {title: "Recycling Info", score: 0.72},│                    │
│  │   ...                                    │                    │
│  │ ]                                        │                    │
│  └─────────────────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Part 4: Testing Search Queries

### 4.1 Direct Search API

Test the `/api/search` endpoint directly:

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "trash pickup", "top_k": 5}'
```

**✅ Expected Output:**
```json
{
  "results": [
    {
      "id": "kb-001",
      "title": "Residential Trash Collection Schedule",
      "content": "Residential trash collection occurs every Monday...",
      "category": "schedule",
      "relevance_score": 0.75
    },
    // ... more results
  ]
}
```

### 4.2 Test Different Queries

Try these queries and observe the results:

| Query | Expected Top Result | Why |
|-------|---------------------|-----|
| `"trash pickup"` | Trash Collection Schedule | Direct keyword match |
| `"garbage collection"` | Trash Collection Schedule | Synonym (demo mode may miss this) |
| `"building permit"` | Building Permit Application | Keyword match |
| `"pothole on my street"` | Report a Pothole | Related topic |
| `"emergency"` | Emergency Services - 911 | Direct match |

### 4.3 Test with Category Filter

Add a category filter:

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "schedule", "category": "schedule", "top_k": 5}'
```

This returns only results from the "schedule" category.

---

## 📖 Part 5: Analyzing Search Results

### 5.1 Understanding Relevance Scores

The `relevance_score` indicates how well a document matches:

| Score Range | Meaning |
|-------------|---------|
| 0.9 - 1.0 | ⭐⭐⭐ Excellent match |
| 0.7 - 0.9 | ⭐⭐ Good match |
| 0.5 - 0.7 | ⭐ Partial match |
| < 0.5 | Weak match |

### 5.2 Full Pipeline Query

Run a complete query through the entire pipeline:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "When is recycling collected?"}'
```

**Examine the response:**
```json
{
  "answer": "Recycling is collected every Wednesday throughout the city...",
  "citations": [
    {
      "entry_id": "kb-002",
      "title": "Recycling Collection Schedule",
      "snippet": "Recycling is collected every Wednesday..."
    }
  ],
  "intent": {
    "category": "schedule",
    "confidence": 0.92
  },
  "reasoning": "Classified as 'schedule' with 92% confidence... Found 4 results..."
}
```

### 5.3 Trace the Reasoning

The `reasoning` field shows you what happened:
1. **Classification**: What category was detected
2. **Search**: How many results were found
3. **Answer**: How the response was generated

---

## 🧪 Hands-On Exercise

### Task: Improve Search Understanding

1. **Run these queries** and fill in the table:

```bash
# Query 1
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I report a broken streetlight?"}'

# Query 2
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Park reservations for birthday party"}'

# Query 3
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the non-emergency police number?"}'
```

| Query | Detected Category | Confidence | # Citations | Top Result Title |
|-------|-------------------|------------|-------------|------------------|
| Streetlight | _________ | ____% | ___ | _________________ |
| Park reservation | _________ | ____% | ___ | _________________ |
| Police number | _________ | ____% | ___ | _________________ |

2. **Find in the code:**
   - What is `search_top_k` set to? (Hint: `app/config.py`)
   - What confidence threshold is used for category filtering? (Hint: `retrieve_agent.py`)

3. **Optional Challenge:**
   Try adding a new entry to `knowledge_base.json` and test if it's searchable:
   ```json
   {
     "id": "kb-999",
     "title": "Library Hours",
     "content": "The public library is open Monday-Saturday 9am-8pm and Sunday 12pm-5pm.",
     "category": "general",
     "service_type": "library",
     "department": "Library Services"
   }
   ```
   Then search for "library hours" - does it appear?

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Understand search tool | Can explain DemoSearchTool vs SearchTool |
| 2 | Know the search algorithm | Can describe how scoring works |
| 3 | Examined knowledge base | Know the data structure and categories |
| 4 | Tested search queries | Got expected results from API |
| 5 | Analyzed relevance scores | Understand what scores mean |
| 6 | Traced full pipeline | Followed query → classification → search → answer |

---

## 📚 Key Concepts

| Term | Definition |
|------|------------|
| **Hybrid Search** | Combining keyword and vector search |
| **Embedding** | Vector representation of text meaning |
| **Relevance Score** | How well a document matches a query (0-1) |
| **Category Filter** | Limiting search to specific document types |
| **Top-K** | Number of results to return |

---

## 🎉 Congratulations!

You've learned how the RAG pipeline retrieves information!

**📊 Progress:**
```
[===============-----] 55% Complete (Exercise 4 of 7)
```

**⏭️ Next:** [Exercise 5: Agent Orchestration](./05-agent-orchestration.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🔍 Exercise 4: Build RAG Pipeline v1.0.0**

</div>
