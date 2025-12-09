# 🔌 Exercise 7: Expose CivicNav as an MCP Server

> ⏱️ **Duration**: 45 minutes | 🎯 **Difficulty**: ⭐⭐⭐ Advanced | 📋 **Prerequisites**: Exercise 0-6 Complete

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-integration-blueviolet) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 🔌 Understand the Model Context Protocol (MCP) architecture | ⬜ |
| 2 | 🛠️ Create an MCP server that wraps CivicNav | ⬜ |
| 3 | 📝 Define MCP tools for your API endpoints | ⬜ |
| 4 | ✅ Test the MCP server with Copilot | ⬜ |
| 5 | 🚀 Deploy the MCP server alongside your API | ⬜ |

---

## 📖 Part 1: Understanding MCP Servers

### 1.1 What is an MCP Server?

In Exercise 2, we *consumed* an MCP server (Azure MCP). Now we'll *create* one!

**MCP Server = Your API exposed as AI-usable tools**

```
┌─────────────────────────────────────────────────────────────────┐
│              🔌 MCP Server Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Before MCP:                                                    │
│  ┌─────────────┐         ┌─────────────┐                       │
│  │ 🤖 AI       │  ❌     │ 🏛️ CivicNav │                       │
│  │   Assistant │ Can't   │    API      │                       │
│  │             │ access  │             │                       │
│  └─────────────┘         └─────────────┘                       │
│                                                                  │
│  After MCP:                                                     │
│  ┌─────────────┐  MCP   ┌─────────────┐  HTTP  ┌───────────┐   │
│  │ 🤖 AI       │◀──────▶│ 🔌 MCP      │◀──────▶│ 🏛️ CivicNav│   │
│  │   Assistant │ tools  │    Server   │  API   │    API     │   │
│  │             │        │             │        │            │   │
│  └─────────────┘        └─────────────┘        └───────────┘   │
│                                                                  │
│  Now Copilot can:                                               │
│  • Query city services                                          │
│  • Search the knowledge base                                    │
│  • Get category information                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 MCP Protocol Overview

MCP uses JSON-RPC over stdio (standard input/output):

| Component | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Actions the AI can take | `civicnav_query`, `civicnav_search` |
| **Resources** | Data the AI can read | Knowledge base entries |
| **Prompts** | Pre-built templates | "Ask about city services" |

### 1.3 Why Create an MCP Server?

| Benefit | Description |
|---------|-------------|
| 🤖 AI Integration | Copilot and other AI tools can use your API directly |
| 🔧 Natural Language | Users ask questions naturally, AI calls your API |
| 🔗 Composability | Combine with other MCP servers (Azure, GitHub, etc.) |
| 📚 Discovery | AI tools auto-discover your capabilities |

---

## 📖 Part 2: MCP Server Structure

### 2.1 Project Structure

We'll create the MCP server in a new folder:

```
📦 civicnav/
├── 📁 app/                    # Existing FastAPI application
├── 📁 mcp_server/             # NEW: MCP server
│   ├── 📄 __init__.py
│   ├── 📄 server.py          # MCP server implementation
│   └── 📄 tools.py           # Tool definitions
├── 📄 mcp_server.py          # Entry point
└── 📄 .vscode/mcp.json       # VS Code configuration
```

### 2.2 The MCP Server Entry Point

Create `mcp_server.py` in the project root:

```python
#!/usr/bin/env python3
"""CivicNav MCP Server - Exposes city services AI as MCP tools."""

import asyncio
import json
import sys
from typing import Any

import httpx


class CivicNavMCPServer:
    """MCP Server that wraps the CivicNav API."""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.client = httpx.AsyncClient(base_url=api_base_url)

    async def handle_request(self, request: dict) -> dict:
        """Handle an incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return self._initialize_response(request_id)
        elif method == "tools/list":
            return self._tools_list_response(request_id)
        elif method == "tools/call":
            return await self._tools_call_response(request_id, params)
        else:
            return self._error_response(request_id, -32601, f"Method not found: {method}")

    def _initialize_response(self, request_id: Any) -> dict:
        """Handle the initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                },
                "serverInfo": {
                    "name": "civicnav",
                    "version": "1.0.0",
                },
            },
        }

    def _tools_list_response(self, request_id: Any) -> dict:
        """Return the list of available tools."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "civicnav_query",
                        "description": "Ask a question about city services. Returns an answer with citations from the knowledge base.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The question about city services (e.g., 'When is trash pickup?')",
                                },
                            },
                            "required": ["query"],
                        },
                    },
                    {
                        "name": "civicnav_search",
                        "description": "Search the city services knowledge base directly. Returns raw search results.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query",
                                },
                                "category": {
                                    "type": "string",
                                    "description": "Filter by category (schedule, permit, event, report, emergency, general)",
                                    "enum": ["schedule", "permit", "event", "report", "emergency", "general"],
                                },
                                "top_k": {
                                    "type": "integer",
                                    "description": "Number of results to return (default: 5)",
                                    "default": 5,
                                },
                            },
                            "required": ["query"],
                        },
                    },
                    {
                        "name": "civicnav_categories",
                        "description": "Get the list of city service categories and how many entries each has.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                ],
            },
        }

    async def _tools_call_response(self, request_id: Any, params: dict) -> dict:
        """Handle a tool call."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "civicnav_query":
                result = await self._call_query(arguments)
            elif tool_name == "civicnav_search":
                result = await self._call_search(arguments)
            elif tool_name == "civicnav_categories":
                result = await self._call_categories()
            else:
                return self._error_response(request_id, -32602, f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2),
                        },
                    ],
                },
            }

        except Exception as e:
            return self._error_response(request_id, -32000, str(e))

    async def _call_query(self, arguments: dict) -> dict:
        """Call the /api/query endpoint."""
        response = await self.client.post(
            "/api/query",
            json={"query": arguments["query"]},
        )
        response.raise_for_status()
        return response.json()

    async def _call_search(self, arguments: dict) -> dict:
        """Call the /api/search endpoint."""
        payload = {"query": arguments["query"]}
        if "category" in arguments:
            payload["category"] = arguments["category"]
        if "top_k" in arguments:
            payload["top_k"] = arguments["top_k"]

        response = await self.client.post("/api/search", json=payload)
        response.raise_for_status()
        return response.json()

    async def _call_categories(self) -> dict:
        """Call the /api/categories endpoint."""
        response = await self.client.get("/api/categories")
        response.raise_for_status()
        return response.json()

    def _error_response(self, request_id: Any, code: int, message: str) -> dict:
        """Return an error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message,
            },
        }

    async def run(self):
        """Run the MCP server, reading from stdin and writing to stdout."""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                if not line:
                    break

                request = json.loads(line)
                response = await self.handle_request(request)
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = self._error_response(None, -32700, str(e))
                print(json.dumps(error_response), flush=True)


async def main():
    """Main entry point."""
    import os
    api_url = os.environ.get("CIVICNAV_API_URL", "http://localhost:8000")
    server = CivicNavMCPServer(api_base_url=api_url)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📖 Part 3: Understanding the Tool Definitions

### 3.1 Tool Schema

Each tool has:

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Unique identifier | `civicnav_query` |
| `description` | What the tool does (AI reads this!) | "Ask a question about city services" |
| `inputSchema` | JSON Schema for parameters | `{ "type": "object", "properties": {...} }` |

### 3.2 The Three CivicNav Tools

```
┌─────────────────────────────────────────────────────────────────┐
│              🛠️ CivicNav MCP Tools                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1️⃣ civicnav_query                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Purpose: Ask questions about city services                  ││
│  │ Input:   query (string, required)                           ││
│  │ Output:  Answer with citations                              ││
│  │ Maps to: POST /api/query                                    ││
│  │                                                              ││
│  │ Example: "When is trash pickup?"                            ││
│  │ Returns: { answer: "Monday and Thursday...", citations: [] }││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  2️⃣ civicnav_search                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Purpose: Search the knowledge base directly                 ││
│  │ Input:   query, category (optional), top_k (optional)       ││
│  │ Output:  Raw search results with scores                     ││
│  │ Maps to: POST /api/search                                   ││
│  │                                                              ││
│  │ Example: query="permit", category="permit"                  ││
│  │ Returns: { results: [{ title: "Building Permit...", ...}] } ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  3️⃣ civicnav_categories                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Purpose: Get available categories                           ││
│  │ Input:   (none)                                             ││
│  │ Output:  Category names and counts                          ││
│  │ Maps to: GET /api/categories                                ││
│  │                                                              ││
│  │ Returns: { categories: [{ name: "schedule", count: 4 },...]}││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Part 4: Configure VS Code to Use the MCP Server

### 4.1 Update .vscode/mcp.json

Open `.vscode/mcp.json` and add the CivicNav server:

```json
{
  "servers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"]
    },
    "civicnav": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "CIVICNAV_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

### 4.2 Understanding the Configuration

| Field | Value | Purpose |
|-------|-------|---------|
| `command` | `python` | What to run |
| `args` | `["mcp_server.py"]` | Script to execute |
| `env` | `{ "CIVICNAV_API_URL": "..." }` | Environment variables |

### 4.3 Restart VS Code

After updating `mcp.json`, restart VS Code for the changes to take effect.

---

## 📖 Part 5: Test the MCP Server

### 5.1 Ensure CivicNav API is Running

In one terminal:
```bash
uvicorn app.main:app --reload --port 8000
```

### 5.2 Test Manually (Optional)

You can test the MCP server directly:

```bash
# Send an initialize request
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python mcp_server.py

# List available tools
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python mcp_server.py
```

### 5.3 Test with Copilot

Open Copilot Chat in VS Code and try these prompts:

**Prompt 1: Ask a city services question**
```
@civicnav When is trash pickup in my neighborhood?
```

**Expected:** Copilot calls `civicnav_query` and returns an answer with citations.

**Prompt 2: Search the knowledge base**
```
@civicnav Search for information about building permits
```

**Expected:** Copilot calls `civicnav_search` with query="building permits".

**Prompt 3: Get categories**
```
@civicnav What categories of city services are available?
```

**Expected:** Copilot calls `civicnav_categories` and lists them.

---

## 📖 Part 6: Test Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│              🔄 MCP Server Test Flow                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User in VS Code Copilot Chat:                                  │
│  "@civicnav When is trash pickup?"                              │
│                    │                                             │
│                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 🤖 Copilot                                                  ││
│  │                                                              ││
│  │ 1. Sees @civicnav mention                                   ││
│  │ 2. Loads civicnav MCP server                                ││
│  │ 3. Gets tool list (civicnav_query, civicnav_search, ...)   ││
│  │ 4. Decides to call civicnav_query                           ││
│  │ 5. Sends: {"name": "civicnav_query",                        ││
│  │           "arguments": {"query": "When is trash pickup?"}}  ││
│  └─────────────────────────────────────────────────────────────┘│
│                    │                                             │
│                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 🔌 MCP Server (mcp_server.py)                               ││
│  │                                                              ││
│  │ 1. Receives tool call                                       ││
│  │ 2. Calls CivicNav API: POST /api/query                      ││
│  │    Body: {"query": "When is trash pickup?"}                 ││
│  │ 3. Gets response with answer and citations                  ││
│  │ 4. Returns result to Copilot                                ││
│  └─────────────────────────────────────────────────────────────┘│
│                    │                                             │
│                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 🏛️ CivicNav API (localhost:8000)                            ││
│  │                                                              ││
│  │ 1. QueryAgent classifies: category=schedule                 ││
│  │ 2. RetrieveAgent searches knowledge base                    ││
│  │ 3. AnswerAgent generates response                           ││
│  │ 4. Returns: {                                               ││
│  │      answer: "Trash pickup is Monday and Thursday...",     ││
│  │      citations: [{title: "Trash Collection Schedule"}]     ││
│  │    }                                                        ││
│  └─────────────────────────────────────────────────────────────┘│
│                    │                                             │
│                    ▼                                             │
│  Copilot displays answer to user:                               │
│  "Trash pickup occurs every Monday and Thursday..."             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Hands-On Exercise

### Task 1: Create the MCP Server

1. **Create the MCP server file:**
   - Copy the code from Part 2 into `mcp_server.py`

2. **Update VS Code configuration:**
   - Add the civicnav server to `.vscode/mcp.json`

3. **Test the server manually:**
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_server.py
```

**Expected Output:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "civicnav_query", ...},
      {"name": "civicnav_search", ...},
      {"name": "civicnav_categories", ...}
    ]
  }
}
```

### Task 2: Test with Copilot

1. **Restart VS Code** after updating mcp.json

2. **Make sure CivicNav API is running:**
```bash
uvicorn app.main:app --reload --port 8000
```

3. **Try these Copilot prompts:**

| Prompt | Expected Tool Called |
|--------|----------------------|
| `@civicnav How do I report a pothole?` | `civicnav_query` |
| `@civicnav Search for emergency services` | `civicnav_search` |
| `@civicnav List all categories` | `civicnav_categories` |

### Task 3: Add a New Tool

**Challenge:** Add a tool that returns the health status of the API.

1. **Add to the tools list:**
```python
{
    "name": "civicnav_health",
    "description": "Check if the CivicNav API is healthy and running.",
    "inputSchema": {
        "type": "object",
        "properties": {},
    },
}
```

2. **Add the handler:**
```python
async def _call_health(self) -> dict:
    """Call the /health endpoint."""
    response = await self.client.get("/health")
    response.raise_for_status()
    return response.json()
```

3. **Update the tool call handler:**
```python
elif tool_name == "civicnav_health":
    result = await self._call_health()
```

4. **Test it:**
```
@civicnav Is the CivicNav service healthy?
```

---

## 📖 Part 7: Deploy MCP Server to Azure

### 7.1 Update azure.yaml

Add the MCP server as a second service:

```yaml
name: civicnav
metadata:
  template: civicnav-agentic-rag

services:
  api:
    project: .
    language: python
    host: containerapp
    docker:
      path: Dockerfile

  mcp:
    project: .
    language: python
    host: containerapp
    docker:
      path: Dockerfile.mcp
```

### 7.2 Create Dockerfile.mcp

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server
COPY mcp_server.py .

# Run the MCP server
CMD ["python", "mcp_server.py"]
```

### 7.3 Deploy

```bash
azd deploy
```

### 7.4 Update VS Code to Use Deployed Server

Update `.vscode/mcp.json` to point to the deployed API:

```json
{
  "servers": {
    "civicnav": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "CIVICNAV_API_URL": "https://civicnav-api-xxxxx.azurecontainerapps.io"
      }
    }
  }
}
```

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | MCP server file created | `mcp_server.py` exists |
| 2 | VS Code configured | `.vscode/mcp.json` has civicnav server |
| 3 | Tools/list works | Manual test returns 3 tools |
| 4 | Copilot can query | `@civicnav` prompts work |
| 5 | All three tools work | Query, search, and categories tested |

---

## 📚 Key Concepts

| Term | Definition |
|------|------------|
| **MCP Server** | A server that exposes tools via the Model Context Protocol |
| **MCP Tool** | An action that an AI can invoke (like a function) |
| **JSON-RPC** | Protocol used for MCP communication |
| **stdio** | Standard input/output - how MCP servers communicate |
| **inputSchema** | JSON Schema defining tool parameters |

---

## 💡 Pro Tips

### Tip 1: Good Tool Descriptions
AI reads your descriptions! Be clear and specific:
```python
# ❌ Bad
"description": "Query API"

# ✅ Good
"description": "Ask a question about city services like trash pickup, permits, or events. Returns a natural language answer with citations."
```

### Tip 2: Handle Errors Gracefully
```python
try:
    result = await self._call_query(arguments)
except httpx.HTTPError as e:
    return self._error_response(request_id, -32000, f"API error: {e}")
```

### Tip 3: Add Logging for Debugging
```python
import logging
logging.basicConfig(level=logging.DEBUG, filename="mcp_server.log")
logger = logging.getLogger(__name__)

async def _call_query(self, arguments):
    logger.debug(f"Calling query with: {arguments}")
    # ...
```

---

## 🎉 Congratulations!

You've completed all exercises! You've built a complete agentic RAG application and exposed it as an MCP server.

**📊 Progress:**
```
[====================] 100% Complete! 🎊
```

**🏆 What You've Accomplished:**
- ✅ Set up a complete development environment
- ✅ Understood AI agents and RAG pipelines
- ✅ Configured Azure MCP for Copilot
- ✅ Used spec-driven development
- ✅ Built a RAG pipeline with hybrid search
- ✅ Orchestrated multiple AI agents
- ✅ Deployed to Azure with azd
- ✅ Created your own MCP server

---

## 🚀 Next Steps

Now that you've completed the lab, consider:

| Direction | Description |
|-----------|-------------|
| 🔧 Add more tools | Create tools for submitting reports, checking status |
| 📊 Add analytics | Track which tools are used most |
| 🔐 Add authentication | Secure your MCP server |
| 🌐 Publish | Share your MCP server with others |
| 📚 Expand knowledge base | Add more city services data |

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🔌 Exercise 7: Expose as MCP Server v1.0.0**

**🎉 You've completed the CivicNav Agentic RAG Lab! 🎉**

</div>
