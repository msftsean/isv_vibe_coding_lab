# 📚 CivicNav Lab Exercises

> 🎓 **Azure AI Engineering Lab** - Build an Agentic RAG Application with GitHub Copilot

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Exercises](https://img.shields.io/badge/exercises-8%20total-blue) | Exercise Count |
| ![Duration](https://img.shields.io/badge/duration-4%20hours-green) | Total Time |
| ![Difficulty](https://img.shields.io/badge/difficulty-beginner%20to%20advanced-yellow) | Skill Level |
| ![Version](https://img.shields.io/badge/version-2.0.0-purple) | Document Version |

---

## 🎯 What You'll Build

**CivicNav** is a city services AI assistant that demonstrates:

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏛️ CivicNav Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Question: "When is trash pickup?"                         │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 🤖 Agentic RAG Pipeline                   │   │
│  │                                                           │   │
│  │   🔍 QueryAgent  →  📚 RetrieveAgent  →  💬 AnswerAgent  │   │
│  │   (Classify)        (Search)             (Generate)       │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         │                                        │
│                         ▼                                        │
│  Answer: "Trash pickup is Monday & Thursday..." [with citations]│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ Learning Path

| Phase | Exercises | Focus | Duration |
|-------|-----------|-------|----------|
| **Foundation** | 0-1 | Setup & Concepts | 45 min |
| **Development** | 2-4 | MCP, Specs, RAG | 85 min |
| **Advanced** | 5-7 | Orchestration, Deploy, MCP Server | 120 min |

---

## 📋 Exercise List

### 🛠️ Exercise 0: Environment Setup
> **Duration:** 20 min | **Difficulty:** ⭐ Beginner

Get your development environment ready with Python, VS Code, and all dependencies.

| What You'll Learn |
|-------------------|
| Install and verify Python 3.11+ |
| Clone and configure the project |
| Start the CivicNav API locally |
| Understand the project structure |

**[Start Exercise 0 →](./00-environment-setup.md)**

---

### 🧠 Exercise 1: Understanding AI Agents & RAG
> **Duration:** 25 min | **Difficulty:** ⭐ Beginner

Learn the core concepts behind AI agents and Retrieval-Augmented Generation.

| What You'll Learn |
|-------------------|
| What AI Agents are and why they matter |
| How RAG (Retrieval-Augmented Generation) works |
| Hybrid search: keyword + vector |
| CivicNav's 3-agent architecture |

**[Start Exercise 1 →](./01-understanding-agents-rag.md)**

---

### 🔌 Exercise 2: Azure MCP Server Setup
> **Duration:** 20 min | **Difficulty:** ⭐ Beginner

Configure VS Code to use Azure MCP with GitHub Copilot Agent Mode.

| What You'll Learn |
|-------------------|
| What MCP (Model Context Protocol) is |
| Configure VS Code Agent Mode |
| Set up Azure MCP Server |
| Query Azure resources with Copilot |

**[Start Exercise 2 →](./02-azure-mcp-setup.md)**

---

### 📝 Exercise 3: Spec-Driven Development
> **Duration:** 20 min | **Difficulty:** ⭐ Beginner

Use specification files to guide AI-assisted code generation.

| What You'll Learn |
|-------------------|
| What spec-driven development means |
| How SPEC.md guides Copilot |
| Generate code following project patterns |
| Verify generated code quality |

**[Start Exercise 3 →](./03-spec-driven-development.md)**

---

### 🔍 Exercise 4: Build RAG Pipeline
> **Duration:** 45 min | **Difficulty:** ⭐⭐ Intermediate

Understand and test the search tool and RetrieveAgent.

| What You'll Learn |
|-------------------|
| DemoSearchTool vs Azure AI Search |
| How hybrid search works |
| RetrieveAgent implementation |
| Test queries and analyze results |

**[Start Exercise 4 →](./04-build-rag-pipeline.md)**

---

### 🔗 Exercise 5: Agent Orchestration
> **Duration:** 40 min | **Difficulty:** ⭐⭐⭐ Advanced

Master how multiple agents work together in a pipeline.

| What You'll Learn |
|-------------------|
| Orchestration patterns (sequential, parallel) |
| BaseAgent abstract class |
| Data flow tracing |
| Pipeline performance analysis |

**[Start Exercise 5 →](./05-agent-orchestration.md)**

---

### 🚀 Exercise 6: Deploy with azd
> **Duration:** 35 min | **Difficulty:** ⭐⭐ Intermediate

Deploy CivicNav to Azure Container Apps with one command.

| What You'll Learn |
|-------------------|
| Install Azure Developer CLI (azd) |
| Understand azure.yaml configuration |
| Deploy with `azd up` |
| Manage environments (dev/staging/prod) |

**[Start Exercise 6 →](./06-deploy-with-azd.md)**

---

### 🔧 Exercise 7: Expose as MCP Server
> **Duration:** 45 min | **Difficulty:** ⭐⭐⭐ Advanced

Create your own MCP server to expose CivicNav to AI assistants.

| What You'll Learn |
|-------------------|
| MCP server architecture |
| Define MCP tools (civicnav_query, civicnav_search) |
| Configure VS Code to use your server |
| Test with GitHub Copilot |

**[Start Exercise 7 →](./07-expose-as-mcp-server.md)**

---

## 📊 Progress Tracker

Use this table to track your progress through the lab:

| # | Exercise | Status | Notes |
|---|----------|--------|-------|
| 0 | 🛠️ Environment Setup | ⬜ | |
| 1 | 🧠 Understanding AI Agents & RAG | ⬜ | |
| 2 | 🔌 Azure MCP Server Setup | ⬜ | |
| 3 | 📝 Spec-Driven Development | ⬜ | |
| 4 | 🔍 Build RAG Pipeline | ⬜ | |
| 5 | 🔗 Agent Orchestration | ⬜ | |
| 6 | 🚀 Deploy with azd | ⬜ | |
| 7 | 🔧 Expose as MCP Server | ⬜ | |

**Progress Bar:**
```
[                    ] 0% - Ready to start!
```

---

## 🏆 Completion Badges

Complete each exercise to earn your badges:

| Badge | Exercise | Requirements |
|-------|----------|--------------|
| 🛠️ **Setup Master** | Exercise 0 | Server running, health check passing |
| 🧠 **AI Concepts** | Exercise 1 | Can explain RAG and agents |
| 🔌 **MCP Integrator** | Exercise 2 | Azure resources accessible via Copilot |
| 📝 **Spec Guru** | Exercise 3 | Generated code follows patterns |
| 🔍 **Search Expert** | Exercise 4 | Queries returning relevant results |
| 🔗 **Orchestrator** | Exercise 5 | Pipeline logs show all stages |
| 🚀 **Cloud Deployer** | Exercise 6 | App running in Azure |
| 🔧 **MCP Creator** | Exercise 7 | Custom MCP server working |

**🎉 Complete all exercises to earn: 🏅 CivicNav Master**

---

## 💡 Tips for Success

### Before You Start
- Ensure you have all prerequisites (Python, VS Code, Git)
- Have your OpenAI API key ready (or use Ollama/Mock mode)
- Read each exercise introduction before starting

### During Exercises
- Follow steps in order - later steps depend on earlier ones
- Use the validation checklists to verify your progress
- Don't skip the hands-on tasks - they reinforce learning

### If You Get Stuck
- Check the Troubleshooting sections in each exercise
- Review the Key Concepts tables
- Try the Pro Tips for advanced techniques

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| 📄 SPEC.md | [Project Specification](../../SPEC.md) |
| 📁 App Code | [app/](../../app/) |
| 📊 Knowledge Base | [data/knowledge_base.json](../../data/knowledge_base.json) |
| ⚙️ Configuration | [.env.example](../../.env.example) |

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12-09 | 🎉 Complete rewrite with comprehensive guides |
| 1.0.0 | 2024-12-09 | ✨ Initial exercise set |

---

<div align="center">

**📚 CivicNav Lab Exercises v2.0.0**

*Build AI-powered applications with Azure and GitHub Copilot*

</div>
