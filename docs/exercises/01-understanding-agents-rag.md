# 🧠 Exercise 1: Understanding AI Agents & RAG

> ⏱️ **Duration**: 25 minutes | 🎯 **Difficulty**: ⭐ Beginner | 📋 **Prerequisites**: Exercise 0 Complete

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-conceptual-purple) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will understand:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 🤖 What AI Agents are and why they matter | ⬜ |
| 2 | 📚 What RAG (Retrieval-Augmented Generation) means | ⬜ |
| 3 | 🔗 How agents and RAG work together | ⬜ |
| 4 | 🏛️ How CivicNav implements these patterns | ⬜ |

---

## 📖 Part 1: What is an AI Agent?

### 🤔 The Problem with Basic LLMs

When you ask ChatGPT a question, it can only use information from its training data. This has limitations:

| Limitation | Example |
|------------|---------|
| 📅 Outdated information | "What's the latest iPhone model?" - may be wrong |
| 🏢 No access to your data | Can't answer "What's in my company's handbook?" |
| 🔧 Can't take actions | Can't actually book a meeting or send an email |

### 💡 Enter AI Agents

An **AI Agent** is an LLM enhanced with:

```
┌─────────────────────────────────────────────────────────┐
│                      🤖 AI Agent                         │
├─────────────────────────────────────────────────────────┤
│  🧠 LLM (Brain)         - Understands language          │
│  🔧 Tools               - Can search, calculate, call APIs│
│  📋 Instructions        - Knows what to do and when     │
│  🔄 Reasoning Loop      - Can plan multi-step tasks     │
└─────────────────────────────────────────────────────────┘
```

**Think of it like this:**
- **LLM alone** = A smart person locked in a room with only their memory
- **AI Agent** = A smart person with a phone, computer, and access to databases

### 🏛️ Agents in CivicNav

CivicNav uses **three specialized agents** working together:

```
User Query: "When is trash pickup?"
                    │
                    ▼
         ┌─────────────────┐
         │ 🔍 QueryAgent   │  "This is about schedules"
         │   (Classifier)  │  "Entity: trash"
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ 📚 RetrieveAgent│  Searches knowledge base
         │   (Searcher)    │  Finds relevant documents
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ 💬 AnswerAgent  │  Writes friendly response
         │   (Writer)      │  Adds citations
         └────────┬────────┘
                  │
                  ▼
         Final Answer with Citations
```

---

## 📖 Part 2: What is RAG?

### 🤔 The Problem

LLMs have a **knowledge cutoff** - they only know what was in their training data. They also **hallucinate** - confidently stating incorrect information.

### 💡 The RAG Solution

**RAG = Retrieval-Augmented Generation**

Instead of relying only on the LLM's memory, we:
1. **Retrieve** relevant documents from a knowledge base
2. **Augment** the LLM's prompt with those documents
3. **Generate** an answer based on the retrieved context

```
┌─────────────────────────────────────────────────────────────────┐
│                    📚 RAG Pipeline                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User: "When is trash pickup?"                                  │
│              │                                                   │
│              ▼                                                   │
│  ┌──────────────────┐                                           │
│  │ 1️⃣ RETRIEVE      │                                           │
│  │                  │    ┌─────────────────────────────┐        │
│  │  Search for      │───▶│ 📄 Doc 1: Trash Schedule    │        │
│  │  relevant docs   │    │ 📄 Doc 2: Recycling Info    │        │
│  │                  │    │ 📄 Doc 3: Holiday Schedule  │        │
│  └──────────────────┘    └─────────────────────────────┘        │
│              │                                                   │
│              ▼                                                   │
│  ┌──────────────────┐                                           │
│  │ 2️⃣ AUGMENT       │                                           │
│  │                  │                                            │
│  │  Combine query   │  "Using these documents, answer:"         │
│  │  + documents     │  [Doc 1] [Doc 2] [Doc 3]                  │
│  │  into prompt     │  "When is trash pickup?"                  │
│  └──────────────────┘                                           │
│              │                                                   │
│              ▼                                                   │
│  ┌──────────────────┐                                           │
│  │ 3️⃣ GENERATE      │                                           │
│  │                  │                                            │
│  │  LLM creates     │  "Trash pickup is Monday & Thursday       │
│  │  grounded answer │   for most areas... [1]"                  │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 Why RAG Matters

| Benefit | Without RAG | With RAG |
|---------|------------|----------|
| 📅 Current info | ❌ Outdated | ✅ Always fresh |
| 🏢 Your data | ❌ Can't access | ✅ Full access |
| 📎 Citations | ❌ None | ✅ Linked sources |
| 🎯 Accuracy | ⚠️ May hallucinate | ✅ Grounded in docs |

---

## 📖 Part 3: Types of Search in RAG

CivicNav uses **hybrid search** - combining three search methods:

### 🔤 Keyword Search

Traditional text matching - finds documents containing the exact words.

```
Query: "trash pickup"
Matches: Documents containing "trash" AND "pickup"
```

**Pros:** Fast, precise for exact terms
**Cons:** Misses synonyms ("garbage collection" wouldn't match)

### 🧮 Vector Search (Semantic)

Uses AI to understand meaning, not just words.

```
Query: "trash pickup" → [0.2, -0.5, 0.8, ...]  (embedding vector)
Docs are also converted to vectors
Finds documents with similar meaning
```

**Pros:** Finds semantically related content
**Cons:** Can be too fuzzy, slower

### 🔀 Hybrid Search (Best of Both)

Combines keyword + vector search with smart ranking.

```
┌──────────────────────────────────────────────────┐
│              🔀 Hybrid Search                     │
├──────────────────────────────────────────────────┤
│                                                   │
│    Query: "When is garbage collection?"          │
│                │                                  │
│        ┌───────┴───────┐                         │
│        ▼               ▼                         │
│   🔤 Keyword      🧮 Vector                      │
│   "garbage"      semantic                        │
│   "collection"   similarity                      │
│        │               │                         │
│        └───────┬───────┘                         │
│                ▼                                  │
│         🏆 Ranked Results                        │
│         1. Trash Collection Schedule ⭐ 0.95     │
│         2. Recycling Information    ⭐ 0.82     │
│         3. Holiday Schedule         ⭐ 0.71     │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## 📖 Part 4: Explore CivicNav's Implementation

### 4.1 View the Agent Files

Open these files in VS Code and read the docstrings:

| File | Purpose | Key Method |
|------|---------|------------|
| `app/agents/base.py` | Abstract base class | `run()` |
| `app/agents/query_agent.py` | Intent classification | `run()` returns `IntentClassification` |
| `app/agents/retrieve_agent.py` | Knowledge search | `run()` returns `list[SearchResult]` |
| `app/agents/answer_agent.py` | Response generation | `run()` returns `QueryResponse` |

### 4.2 Trace a Request

Let's follow what happens when you ask "When is trash pickup?"

**Step 1: Open `app/main.py`** and find the `/api/query` endpoint:

```python
@app.post("/api/query")
async def query(request: QueryRequest) -> QueryResponse:
    # 1. QueryAgent classifies intent
    # 2. RetrieveAgent searches knowledge base
    # 3. AnswerAgent generates response
```

**Step 2: Open `app/agents/query_agent.py`**:

The QueryAgent sends this prompt to the LLM:
```
You are a city services query classifier. Analyze the user query and return a JSON object with:
1. category: The service category (schedule, event, report, permit, emergency, general)
2. confidence: Your confidence score from 0.0 to 1.0
3. entities: Extracted entities (dates, locations, service types)
```

**Step 3: Open `app/agents/retrieve_agent.py`**:

The RetrieveAgent:
1. Creates an embedding of the query
2. Searches the knowledge base using hybrid search
3. Returns ranked results

**Step 4: Open `app/agents/answer_agent.py`**:

The AnswerAgent:
1. Receives the query + search results
2. Prompts the LLM to write a helpful response
3. Includes citations to source documents

### 4.3 Test with Different Queries

Try these queries and observe the different responses:

| Query | Expected Category | Why |
|-------|------------------|-----|
| "When is trash pickup?" | `schedule` | Asking about recurring service |
| "How do I get a building permit?" | `permit` | Permit-related question |
| "There's a pothole on Main St" | `report` | Issue report |
| "What events are happening this weekend?" | `event` | Community events |
| "I need to call 911" | `emergency` | Emergency services |

Test command:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR_QUERY_HERE"}'
```

---

## 🧪 Hands-On Exercise

### Task: Analyze the Agent Pipeline

1. **Make a query** to the API:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I report a pothole?"}'
```

2. **Look at the response** and answer these questions:

| Question | Your Answer |
|----------|-------------|
| What category was detected? | _____________ |
| What was the confidence score? | _____________ |
| How many citations were included? | _____________ |
| What was the latency (ms)? | _____________ |

3. **Find in the code** (hint: use Ctrl+Shift+F to search):
   - Where is the category list defined?
   - What temperature is used for classification?
   - How many search results are retrieved?

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Can explain what an AI Agent is | Write a 1-sentence definition |
| 2 | Can explain RAG | Describe the 3 steps |
| 3 | Understand hybrid search | Name the 2 search types combined |
| 4 | Know CivicNav's 3 agents | Name them and their purpose |
| 5 | Traced a request through code | Found the key methods |

---

## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **AI Agent** | An LLM enhanced with tools, instructions, and reasoning capabilities |
| **RAG** | Retrieval-Augmented Generation - grounding LLM responses in retrieved documents |
| **Embedding** | A vector (list of numbers) representing the meaning of text |
| **Hybrid Search** | Combining keyword and semantic search for better results |
| **Intent Classification** | Determining what category a user's question belongs to |
| **Citation** | A reference to the source document used to generate an answer |

---

## 🎉 Congratulations!

You now understand the core concepts behind AI Agents and RAG!

**📊 Progress:**
```
[========------------] 20% Complete (Exercise 1 of 7)
```

**⏭️ Next:** [Exercise 2: Azure MCP Server Setup](./02-azure-mcp-setup.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🧠 Exercise 1: Understanding AI Agents & RAG v1.0.0**

</div>
