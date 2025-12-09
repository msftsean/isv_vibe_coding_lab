# 🔗 Exercise 5: Agent Orchestration

> ⏱️ **Duration**: 40 minutes | 🎯 **Difficulty**: ⭐⭐⭐ Advanced | 📋 **Prerequisites**: Exercise 0-4 Complete

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-architecture-purple) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 🔗 Understand how agents are orchestrated together | ⬜ |
| 2 | 📊 Trace data flow through the complete pipeline | ⬜ |
| 3 | 🔧 Understand the BaseAgent abstract class | ⬜ |
| 4 | 🧪 Modify the orchestration logic | ⬜ |
| 5 | 📈 Analyze pipeline performance metrics | ⬜ |

---

## 📖 Part 1: Understanding Agent Orchestration

### 1.1 What is Agent Orchestration?

**Orchestration** is how multiple agents work together to complete a task. Think of it like an orchestra:

```
┌─────────────────────────────────────────────────────────────────┐
│                  🎼 Agent Orchestration                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Orchestra Analogy:                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │ 🎻       │   │ 🎺       │   │ 🥁       │   │ 🎹       │     │
│  │ Violins  │   │ Brass    │   │ Percussion│   │ Piano    │     │
│  │          │   │          │   │          │   │          │     │
│  │ Play     │   │ Play     │   │ Play     │   │ Play     │     │
│  │ strings  │   │ brass    │   │ rhythm   │   │ melody   │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘     │
│        │             │              │              │            │
│        └─────────────┴──────────────┴──────────────┘            │
│                            │                                     │
│                   🎼 Conductor (Orchestrator)                   │
│                   Coordinates all sections                       │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CivicNav Agents:                                               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                    │
│  │ 🔍       │   │ 📚       │   │ 💬       │                    │
│  │ Query    │   │ Retrieve │   │ Answer   │                    │
│  │ Agent    │   │ Agent    │   │ Agent    │                    │
│  │          │   │          │   │          │                    │
│  │ Classify │──▶│ Search   │──▶│ Generate │                    │
│  │ intent   │   │ docs     │   │ response │                    │
│  └──────────┘   └──────────┘   └──────────┘                    │
│        │             │              │                           │
│        └─────────────┴──────────────┘                           │
│                      │                                          │
│             ⚡ main.py (Orchestrator)                           │
│             Coordinates agent pipeline                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Sequential vs Parallel Orchestration

| Pattern | Description | Example |
|---------|-------------|---------|
| **Sequential** | Agents run one after another | Query → Retrieve → Answer |
| **Parallel** | Agents run simultaneously | Multiple searches at once |
| **Conditional** | Next agent depends on result | Skip search if emergency |
| **Iterative** | Repeat until condition met | Refine answer until quality threshold |

**CivicNav uses sequential orchestration** because each agent needs the previous agent's output.

---

## 📖 Part 2: The BaseAgent Pattern

### 2.1 Open the Base Agent Class

Open `app/agents/base.py` and examine the abstract base class:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseAgent(ABC, Generic[InputType, OutputType]):
    """Abstract base class for all agents in the pipeline."""

    def __init__(self, name: str) -> None:
        """Initialize the agent with a name."""
        self.name = name
        self.tools_used: list[str] = []

    @abstractmethod
    async def run(self, input_data: InputType) -> AgentResult:
        """Execute the agent's main logic.

        Args:
            input_data: The input data for this agent

        Returns:
            AgentResult containing the output and metadata
        """
        pass
```

### 2.2 Key Concepts

| Concept | Purpose | Benefit |
|---------|---------|---------|
| `ABC` | Abstract Base Class | Forces all agents to implement `run()` |
| `Generic[InputType, OutputType]` | Type parameters | Type safety for inputs/outputs |
| `AgentResult` | Standard return type | Consistent output structure |
| `tools_used` | Track which tools were called | Debugging and logging |

### 2.3 The AgentResult Structure

```python
@dataclass
class AgentResult(Generic[T]):
    """Standardized result from any agent."""
    output: T                    # The actual result data
    reasoning: str              # Explanation of what the agent did
    tools_used: list[str]       # Which tools were called
    latency_ms: float = 0.0     # How long it took
```

**Why use AgentResult?**
- Consistent structure across all agents
- Easy to log and debug
- Can add metadata without changing interfaces

---

## 📖 Part 3: Tracing the Complete Pipeline

### 3.1 The Orchestrator in main.py

Open `app/main.py` and find the `/api/query` endpoint:

```python
@app.post("/api/query")
async def query(request: QueryRequest) -> QueryResponse:
    """Process a user query through the agent pipeline."""
    start_time = time.time()

    # Step 1: Classify intent
    query_agent = QueryAgent()
    classification_result = await query_agent.run(request.query)
    classification = classification_result.output

    # Step 2: Retrieve relevant documents
    retrieve_agent = RetrieveAgent()
    retrieve_result = await retrieve_agent.run(classification)
    search_results = retrieve_result.output

    # Step 3: Generate answer
    answer_agent = AnswerAgent()
    answer_result = await answer_agent.run(
        AnswerInput(
            query=request.query,
            classification=classification,
            search_results=search_results,
        )
    )

    # Calculate total latency
    latency_ms = (time.time() - start_time) * 1000

    return QueryResponse(
        id=str(uuid.uuid4()),
        answer=answer_result.output.answer,
        citations=answer_result.output.citations,
        intent=classification,
        latency_ms=latency_ms,
    )
```

### 3.2 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│            📊 Complete Pipeline Data Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📥 INPUT                                                        │
│  QueryRequest { query: "When is trash pickup?" }                │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 🔍 STAGE 1: QueryAgent.run(query)                        │   │
│  │                                                           │   │
│  │   Input:  "When is trash pickup?"                        │   │
│  │                    │                                      │   │
│  │                    ▼                                      │   │
│  │   ┌────────────────────────────────────────────┐         │   │
│  │   │ 🧠 LLM Call: "Classify this query..."     │         │   │
│  │   │    Model: gpt-4o-mini                      │         │   │
│  │   │    Temperature: 0.0 (deterministic)        │         │   │
│  │   └────────────────────────────────────────────┘         │   │
│  │                    │                                      │   │
│  │   Output: IntentClassification {                         │   │
│  │     category: "schedule",                                │   │
│  │     confidence: 0.95,                                    │   │
│  │     entities: [{type: "service", value: "trash"}]        │   │
│  │   }                                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 📚 STAGE 2: RetrieveAgent.run(classification)            │   │
│  │                                                           │   │
│  │   Input: IntentClassification                            │   │
│  │                    │                                      │   │
│  │                    ▼                                      │   │
│  │   ┌────────────────────────────────────────────┐         │   │
│  │   │ 🔎 Create embedding for "When is trash..." │         │   │
│  │   │ 🔎 Hybrid search with category filter      │         │   │
│  │   │    • Keyword: "trash", "pickup"            │         │   │
│  │   │    • Vector: semantic similarity           │         │   │
│  │   │    • Filter: category="schedule"           │         │   │
│  │   └────────────────────────────────────────────┘         │   │
│  │                    │                                      │   │
│  │   Output: list[SearchResult] [                           │   │
│  │     {title: "Trash Schedule", score: 0.95},              │   │
│  │     {title: "Recycling Info", score: 0.82},              │   │
│  │     {title: "Holiday Schedule", score: 0.71}             │   │
│  │   ]                                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 💬 STAGE 3: AnswerAgent.run(AnswerInput)                 │   │
│  │                                                           │   │
│  │   Input: AnswerInput {                                   │   │
│  │     query: "When is trash pickup?",                      │   │
│  │     classification: IntentClassification,                │   │
│  │     search_results: list[SearchResult]                   │   │
│  │   }                                                      │   │
│  │                    │                                      │   │
│  │                    ▼                                      │   │
│  │   ┌────────────────────────────────────────────┐         │   │
│  │   │ 🧠 LLM Call: "Answer based on documents..." │         │   │
│  │   │    Context: [Doc 1] [Doc 2] [Doc 3]        │         │   │
│  │   │    Instructions: Be helpful, cite sources  │         │   │
│  │   └────────────────────────────────────────────┘         │   │
│  │                    │                                      │   │
│  │   Output: AnswerOutput {                                 │   │
│  │     answer: "Trash pickup is Monday & Thursday...",      │   │
│  │     citations: [{id: "kb-001", title: "Trash..."}]       │   │
│  │   }                                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  📤 OUTPUT                                                       │
│  QueryResponse {                                                 │
│    id: "uuid-...",                                              │
│    answer: "Trash pickup is Monday & Thursday...",              │
│    citations: [...],                                            │
│    intent: { category: "schedule", confidence: 0.95 },          │
│    latency_ms: 5500                                             │
│  }                                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Part 4: Examining Each Agent

### 4.1 QueryAgent Deep Dive

Open `app/agents/query_agent.py`:

```python
class QueryAgent(BaseAgent[str, IntentClassification]):
    """Agent for classifying user intent and extracting entities."""

    SYSTEM_PROMPT = """You are a city services query classifier.
    Analyze the user query and return a JSON object with:
    - category: One of (schedule, permit, event, report, emergency, general)
    - confidence: Your confidence score from 0.0 to 1.0
    - entities: Extracted entities like dates, locations, service types
    """

    async def run(self, input_data: str) -> AgentResult:
        """Classify the user's query."""
        response = await self.openai_tool.chat_completion(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": input_data},
            ],
            temperature=0.0,  # Deterministic for classification
        )
        # Parse JSON response into IntentClassification
        classification = IntentClassification.model_validate_json(response)
        return AgentResult(output=classification, ...)
```

**Key Points:**
| Aspect | Value | Why |
|--------|-------|-----|
| Temperature | 0.0 | Classification should be consistent |
| Output | JSON | Structured data for downstream agents |
| Generic Types | `str` → `IntentClassification` | Clear contract |

### 4.2 RetrieveAgent Deep Dive

Open `app/agents/retrieve_agent.py`:

```python
class RetrieveAgent(BaseAgent[IntentClassification, list[SearchResult]]):
    """Agent for retrieving relevant documents from the knowledge base."""

    async def run(self, input_data: IntentClassification) -> AgentResult:
        """Search for relevant documents."""
        query = input_data.original_query

        # Create embedding for semantic search
        embedding = await self.openai_tool.create_embedding(query)

        # Perform hybrid search
        results = await self.search_tool.hybrid_search(
            query=query,
            vector=embedding,
            top_k=self.settings.search_top_k,
            category=input_data.category if input_data.confidence > 0.7 else None,
        )

        return AgentResult(output=results, ...)
```

**Key Points:**
| Aspect | Value | Why |
|--------|-------|-----|
| Category Filter | Only if confidence > 0.7 | Don't filter on uncertain classifications |
| Hybrid Search | Keyword + Vector | Better recall than either alone |
| top_k | Configurable | Balance between context and cost |

### 4.3 AnswerAgent Deep Dive

Open `app/agents/answer_agent.py`:

```python
class AnswerAgent(BaseAgent[AnswerInput, AnswerOutput]):
    """Agent for generating the final answer with citations."""

    SYSTEM_PROMPT = """You are a helpful city services assistant.
    Answer the user's question based ONLY on the provided documents.
    Include citations in [1], [2] format referencing the document IDs.
    If the documents don't contain the answer, say so politely.
    """

    async def run(self, input_data: AnswerInput) -> AgentResult:
        """Generate the final answer."""
        # Build context from search results
        context = self._build_context(input_data.search_results)

        response = await self.openai_tool.chat_completion(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {input_data.query}"},
            ],
            temperature=0.7,  # Some creativity for natural responses
        )

        return AgentResult(output=AnswerOutput(answer=response, citations=...), ...)
```

**Key Points:**
| Aspect | Value | Why |
|--------|-------|-----|
| Temperature | 0.7 | Natural-sounding responses |
| Context | From search results | RAG grounding |
| Citations | Required | Verifiability |

---

## 📖 Part 5: Performance Analysis

### 5.1 Understanding Latency

The total latency is the sum of all stages:

```
┌─────────────────────────────────────────────────────────────────┐
│              ⏱️ Pipeline Latency Breakdown                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Total: ~5500ms (with OpenAI API)                               │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ QueryAgent  │  │RetrieveAgent│  │ AnswerAgent │             │
│  │             │  │             │  │             │             │
│  │ ~1500ms     │  │ ~1500ms     │  │ ~2500ms     │             │
│  │             │  │             │  │             │             │
│  │ • LLM call  │  │ • Embedding │  │ • LLM call  │             │
│  │   for       │  │   creation  │  │   with      │             │
│  │   classify  │  │ • Search    │  │   context   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│        │                │                │                      │
│        └────────────────┴────────────────┘                      │
│                         │                                       │
│               Total: 5500ms                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Test and Measure

Run a query and examine the latency:

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "When is trash pickup?"}' | jq '.latency_ms'
```

**Expected Output:**
```
5500
```

### 5.3 Latency by Configuration

| Configuration | Expected Latency | Notes |
|---------------|------------------|-------|
| OpenAI API (gpt-4o-mini) | ~5-6 seconds | Fast, high quality |
| OpenAI API (gpt-4o) | ~8-10 seconds | Slower, better quality |
| Ollama (phi3:mini) | ~60-90 seconds | Local, no API cost |
| Mock mode | ~100ms | For testing only |

---

## 🧪 Hands-On Exercise

### Task 1: Trace a Query Through Logs

1. **Enable debug logging** by adding to `app/config.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Run a query** and observe the logs:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I get a building permit?"}'
```

3. **Answer these questions:**

| Question | Your Answer |
|----------|-------------|
| What category was detected? | _____________ |
| How many search results were returned? | _____________ |
| What was the total latency? | _____________ |
| How many LLM calls were made? | _____________ |

### Task 2: Modify the Pipeline

1. **Add logging to track pipeline flow:**

Open `app/main.py` and add logging statements:

```python
import logging
logger = logging.getLogger(__name__)

@app.post("/api/query")
async def query(request: QueryRequest) -> QueryResponse:
    logger.info(f"📥 Received query: {request.query}")

    # Step 1
    logger.info("🔍 Stage 1: Running QueryAgent...")
    classification_result = await query_agent.run(request.query)
    logger.info(f"🔍 Stage 1 complete: category={classification_result.output.category}")

    # Step 2
    logger.info("📚 Stage 2: Running RetrieveAgent...")
    retrieve_result = await retrieve_agent.run(classification_result.output)
    logger.info(f"📚 Stage 2 complete: found {len(retrieve_result.output)} results")

    # Step 3
    logger.info("💬 Stage 3: Running AnswerAgent...")
    answer_result = await answer_agent.run(...)
    logger.info("💬 Stage 3 complete")

    logger.info(f"📤 Total latency: {latency_ms:.0f}ms")
    return response
```

2. **Test the enhanced logging:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What events are happening this weekend?"}'
```

### Task 3: Experiment with Agent Parameters

1. **Find these configuration values:**

| Setting | File | Current Value |
|---------|------|---------------|
| Classification temperature | `query_agent.py` | _________ |
| Search top_k | `config.py` | _________ |
| Answer temperature | `answer_agent.py` | _________ |

2. **Experiment:**
   - What happens if you increase the answer temperature to 1.0?
   - What happens if you reduce top_k to 1?
   - What happens if classification temperature is 1.0?

---

## 📖 Part 6: Advanced Orchestration Patterns

### 6.1 Error Handling in Pipeline

The current pipeline can be enhanced with error handling:

```python
@app.post("/api/query")
async def query(request: QueryRequest) -> QueryResponse:
    try:
        # Stage 1
        classification_result = await query_agent.run(request.query)
    except Exception as e:
        logger.error(f"QueryAgent failed: {e}")
        # Fallback: assume general category
        classification_result = AgentResult(
            output=IntentClassification(category=Category.GENERAL, confidence=0.5),
            reasoning="Fallback due to classification error",
        )

    try:
        # Stage 2
        retrieve_result = await retrieve_agent.run(classification_result.output)
    except Exception as e:
        logger.error(f"RetrieveAgent failed: {e}")
        # Fallback: return empty results
        retrieve_result = AgentResult(output=[], reasoning="Search unavailable")

    # Stage 3 always runs with whatever we have
    answer_result = await answer_agent.run(...)
```

### 6.2 Conditional Orchestration

For emergency queries, you might skip certain stages:

```python
@app.post("/api/query")
async def query(request: QueryRequest) -> QueryResponse:
    # Check for emergency keywords
    emergency_keywords = ["911", "emergency", "fire", "ambulance", "police"]
    is_emergency = any(kw in request.query.lower() for kw in emergency_keywords)

    if is_emergency:
        # Skip classification, go straight to emergency response
        return QueryResponse(
            answer="For emergencies, please call 911 immediately.",
            intent=IntentClassification(category=Category.EMERGENCY, confidence=1.0),
        )

    # Normal pipeline for non-emergency queries
    ...
```

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Understand orchestration | Can explain sequential vs parallel patterns |
| 2 | Know BaseAgent pattern | Can describe the abstract class structure |
| 3 | Traced data flow | Can explain what data passes between agents |
| 4 | Added pipeline logging | Logs show each stage's progress |
| 5 | Know latency breakdown | Can estimate time for each stage |
| 6 | Understand error handling | Can describe fallback strategies |

---

## 📚 Key Concepts

| Term | Definition |
|------|------------|
| **Orchestration** | Coordinating multiple agents to complete a task |
| **Sequential Pipeline** | Agents run one after another in order |
| **AgentResult** | Standard wrapper for agent outputs with metadata |
| **BaseAgent** | Abstract class defining the agent interface |
| **Latency** | Total time from request to response |

---

## 💡 Pro Tips

### Tip 1: Use Structured Logging
```python
logger.info(f"Stage complete", extra={
    "stage": "QueryAgent",
    "category": classification.category,
    "confidence": classification.confidence,
    "latency_ms": latency,
})
```

### Tip 2: Consider Parallel Execution
For independent operations, use `asyncio.gather`:
```python
results = await asyncio.gather(
    search_tool.keyword_search(query),
    search_tool.vector_search(query),
)
```

### Tip 3: Cache Repeated Operations
If the same query comes in multiple times, cache the result:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_classification(query: str):
    return query_agent.run(query)
```

---

## 🎉 Congratulations!

You've mastered agent orchestration! You understand how multiple agents work together.

**📊 Progress:**
```
[================----] 70% Complete (Exercise 5 of 7)
```

**⏭️ Next:** [Exercise 6: Deploy with azd](./06-deploy-with-azd.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🔗 Exercise 5: Agent Orchestration v1.0.0**

</div>
