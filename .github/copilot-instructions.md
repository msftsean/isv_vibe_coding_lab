# 🤖 CivicNav Copilot Instructions

> 🏛️ You are helping develop CivicNav, a city services Q&A application using Azure AI services.

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Copilot](https://img.shields.io/badge/copilot-enabled-brightgreen) | Integration |
| ![Agent Mode](https://img.shields.io/badge/agent%20mode-active-blue) | Mode |

---

## 📋 Version History

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0.0 | 2024-12-09 | ✨ Complete instructions with all patterns | ✅ Current |
| 0.5.0 | 2024-12-07 | 🚧 Initial draft | 📦 Archived |

---

## 🏗️ Architecture

CivicNav uses a three-stage agentic RAG pipeline:

| Stage | Agent | Responsibility |
|-------|-------|----------------|
| 1️⃣ | 🔍 **QueryAgent** | Classifies intent (schedule, event, report, permit, emergency, general) and extracts entities |
| 2️⃣ | 📚 **RetrieveAgent** | Performs hybrid search using Azure AI Search (vector + keyword + semantic ranking) |
| 3️⃣ | 💬 **AnswerAgent** | Synthesizes natural language responses with citations from Azure OpenAI |

---

## 🔑 Key Patterns

### 🔐 Azure Authentication

Always use `DefaultAzureCredential` for Azure service authentication:

```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
```

---

### ⚡ Async-First

All Azure SDK calls should be async:

```python
async def search(self, query: str) -> list[SearchResult]:
    results = await self.client.search(...)
    return results
```

---

### 📊 Pydantic Models

Use Pydantic v2 for all data models:

```python
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
```

---

### 🤖 Agent Pattern

Agents inherit from BaseAgent and implement async run():

```python
class MyAgent(BaseAgent[InputType, OutputType]):
    async def run(self, input_data: InputType) -> AgentResult:
        # Implementation
        return AgentResult(output=result, reasoning="...", tools_used=self.tools_used)
```

---

## 📁 Project Structure

| Directory | Purpose | Status |
|-----------|---------|--------|
| 🤖 `app/agents/` | Agent implementations | ✅ Ready |
| 🔧 `app/tools/` | Azure SDK wrappers | ✅ Ready |
| 📊 `app/models/` | Pydantic schemas | ✅ Ready |
| 🔌 `app/mcp/` | MCP server | ✅ Ready |
| ☁️ `infra/` | Bicep templates | ✅ Ready |
| 📚 `data/` | Knowledge base | ✅ Ready |

---

## 🔌 Available MCP Tools

When Azure MCP Server is configured, you have access to:

| Tool | Description | Status |
|------|-------------|--------|
| ☁️ Azure resource management | Manage Azure resources | ✅ Available |
| 🔍 CivicNav query tools | Query city services | ✅ Available |
| 📚 CivicNav search tools | Search knowledge base | ✅ Available |

---

## 🧪 Testing

Use pytest with Azure mocks:

```python
@pytest.mark.asyncio
async def test_agent(mock_openai_tool):
    agent = MyAgent()
    result = await agent.execute(input_data)
    assert result.output is not None
```

---

<div align="center">

**🤖 Copilot Instructions v1.0.0**

</div>
