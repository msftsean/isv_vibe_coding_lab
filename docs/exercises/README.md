# 📚 Lab Exercises

> 🎓 Hands-on exercises for mastering Azure AI engineering patterns.

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Exercises](https://img.shields.io/badge/exercises-6%20total-blue) | Count |
| ![Duration](https://img.shields.io/badge/duration-2.5%20hours-green) | Time |
| ![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow) | Level |

---

## 📋 Version History

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0.0 | 2024-12-09 | ✨ Complete exercise set with validations | ✅ Current |
| 0.5.0 | 2024-12-07 | 🚧 Draft exercises | 📦 Archived |

---

## 🔌 Exercise 1: Azure MCP Server Setup (15 min)

> Configure `.vscode/mcp.json` for Copilot Agent Mode integration.

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Open VS Code settings and enable Agent Mode | ⬜ Todo |
| 2️⃣ | Review the MCP configuration in `.vscode/mcp.json` | ⬜ Todo |
| 3️⃣ | Start the Azure MCP Server: `npx -y @azure/mcp@latest server start` | ⬜ Todo |
| 4️⃣ | Test by asking Copilot to list Azure resources | ⬜ Todo |

**✅ Validation:** Copilot can respond to Azure resource queries

---

## 📝 Exercise 2: Spec-Driven Development (15 min)

> Review SPEC.md and scaffold code with Copilot.

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Read `SPEC.md` to understand requirements | ⬜ Todo |
| 2️⃣ | Ask Copilot to explain the architecture | ⬜ Todo |
| 3️⃣ | Use Copilot to generate a new model following existing patterns | ⬜ Todo |

**✅ Validation:** Generated code follows project conventions

---

## 🔍 Exercise 3: Build RAG Pipeline (45 min)

> Implement hybrid search in `retrieve_agent.py`.

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Review `app/tools/search_tool.py` for search capabilities | ⬜ Todo |
| 2️⃣ | Understand vector, keyword, and semantic search | ⬜ Todo |
| 3️⃣ | Implement the `run()` method in RetrieveAgent | ⬜ Todo |
| 4️⃣ | Test with sample queries | ⬜ Todo |

**✅ Validation:** Search returns relevant results with scores

---

## 🤖 Exercise 4: Agent Orchestration (30 min)

> Wire the query-retrieve-answer pipeline in `main.py`.

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Review the three agents (Query, Retrieve, Answer) | ⬜ Todo |
| 2️⃣ | Understand data flow between agents | ⬜ Todo |
| 3️⃣ | Implement the pipeline in the `/api/query` endpoint | ⬜ Todo |
| 4️⃣ | Test end-to-end with the chat UI | ⬜ Todo |

**✅ Validation:** Complete answers with citations returned

---

## ☁️ Exercise 5: Deploy with azd (20 min)

> Deploy to Azure with one command.

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Review `azure.yaml` and `infra/main.bicep` | ⬜ Todo |
| 2️⃣ | Run `azd up` to provision and deploy | ⬜ Todo |
| 3️⃣ | Verify deployment in Azure portal | ⬜ Todo |
| 4️⃣ | Test the deployed endpoint | ⬜ Todo |

**✅ Validation:** Application accessible via Container Apps URL

---

## 🔧 Exercise 6: Expose as MCP Server (15 min)

> Implement MCP tools for AI assistant integration.

| Step | Task | Status |
|------|------|--------|
| 1️⃣ | Review `app/mcp/server.py` | ⬜ Todo |
| 2️⃣ | Understand the tool schema definitions | ⬜ Todo |
| 3️⃣ | Test tools via Copilot Agent Mode | ⬜ Todo |
| 4️⃣ | Try: "Use CivicNav to find trash pickup schedule" | ⬜ Todo |

**✅ Validation:** Copilot uses CivicNav tools successfully

---

## 🚀 Extension Challenge: Multi-turn Conversations

> Add conversation memory for follow-up questions.

| Hint | Description |
|------|-------------|
| 💡 | Store session history in a dict keyed by session_id |
| 💡 | Pass conversation context to AnswerAgent |
| 💡 | Implement session timeout/cleanup |

---

## 📊 Exercise Summary

| # | Exercise | ⏱️ Duration | 🎯 Focus | Difficulty |
|---|----------|-------------|----------|------------|
| 1 | 🔌 Azure MCP Server Setup | 15 min | Configuration | ⭐ Easy |
| 2 | 📝 Spec-Driven Development | 15 min | Code Generation | ⭐ Easy |
| 3 | 🔍 Build RAG Pipeline | 45 min | Search Implementation | ⭐⭐ Medium |
| 4 | 🤖 Agent Orchestration | 30 min | Pipeline Integration | ⭐⭐ Medium |
| 5 | ☁️ Deploy with azd | 20 min | Cloud Deployment | ⭐ Easy |
| 6 | 🔧 Expose as MCP Server | 15 min | Tool Integration | ⭐⭐ Medium |
| 🌟 | Multi-turn Conversations | Bonus | State Management | ⭐⭐⭐ Hard |

---

<div align="center">

**📚 Lab Exercises v1.0.0**

</div>
