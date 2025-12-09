# 🛠️ Exercise 0: Environment Setup

> ⏱️ **Duration**: 20 minutes | 🎯 **Difficulty**: ⭐ Beginner | 📋 **Prerequisites**: None

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Tested](https://img.shields.io/badge/tested-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen) | Platform Support |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | ✅ Have Python 3.11+ installed and working | ⬜ |
| 2 | ✅ Have VS Code with GitHub Copilot configured | ⬜ |
| 3 | ✅ Have the CivicNav project cloned and dependencies installed | ⬜ |
| 4 | ✅ Have the application running locally | ⬜ |
| 5 | ✅ Understand the project structure | ⬜ |

---

## 📚 What You'll Need

Before starting, ensure you have:

| Tool | Version | Download Link | Purpose |
|------|---------|---------------|---------|
| 🐍 Python | 3.11+ | [python.org](https://python.org/downloads) | Runtime |
| 📝 VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com) | IDE |
| 🤖 GitHub Copilot | Extension | [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) | AI Assistant |
| 📦 Git | Latest | [git-scm.com](https://git-scm.com) | Version Control |

---

## 📖 Step 1: Verify Python Installation

### 1.1 Check Python Version

Open a terminal and run:

```bash
python --version
```

**✅ Expected Output:**
```
Python 3.11.x  (or 3.12.x, 3.13.x)
```

**❌ If you see Python 2.x or "command not found":**

| Platform | Solution |
|----------|----------|
| 🪟 Windows | Download from [python.org](https://python.org) - check "Add to PATH" during install |
| 🍎 macOS | Run `brew install python@3.11` or download from python.org |
| 🐧 Linux | Run `sudo apt install python3.11` or equivalent |

### 1.2 Verify pip

```bash
pip --version
```

**✅ Expected Output:**
```
pip 23.x.x from ... (python 3.11)
```

---

## 📖 Step 2: Clone the Repository

### 2.1 Navigate to Your Projects Folder

```bash
# Windows
cd C:\Users\YourName\repos

# macOS/Linux
cd ~/repos
```

### 2.2 Clone CivicNav

```bash
git clone https://github.com/your-org/civicnav.git
cd civicnav
```

**✅ Expected Output:**
```
Cloning into 'civicnav'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
```

---

## 📖 Step 3: Create Virtual Environment

### 3.1 Create the Virtual Environment

```bash
python -m venv .venv
```

### 3.2 Activate the Virtual Environment

| Platform | Command |
|----------|---------|
| 🪟 Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| 🪟 Windows (CMD) | `.venv\Scripts\activate.bat` |
| 🍎 macOS / 🐧 Linux | `source .venv/bin/activate` |

**✅ Expected Result:**
Your terminal prompt should now show `(.venv)` at the beginning:
```
(.venv) C:\Users\YourName\repos\civicnav>
```

### 🔧 Troubleshooting: PowerShell Execution Policy

If you get an error about "running scripts is disabled", run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📖 Step 4: Install Dependencies

### 4.1 Install Python Packages

```bash
pip install -r requirements.txt
```

**✅ Expected Output:**
```
Installing collected packages: ...
Successfully installed fastapi-0.115.0 uvicorn-0.30.0 pydantic-2.8.0 ...
```

This installs:
| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework for our API |
| `uvicorn` | ASGI server to run the app |
| `pydantic` | Data validation |
| `openai` | OpenAI/Azure OpenAI client |
| `httpx` | Async HTTP client |

---

## 📖 Step 5: Configure Environment Variables

### 5.1 Create Your .env File

```bash
# Copy the example file
cp .env.example .env
```

Or on Windows:
```cmd
copy .env.example .env
```

### 5.2 Edit .env with Your API Key

Open `.env` in VS Code and add your OpenAI API key:

```env
# Option 1: OpenAI API (recommended - fast, high quality)
OPENAI_API_KEY=sk-your-api-key-here
USE_OPENAI=true
USE_OLLAMA=false
```

**🔑 Don't have an API key?** You have three options:

| Option | Setup | Speed | Quality |
|--------|-------|-------|---------|
| 🌐 OpenAI API | Get key from [platform.openai.com](https://platform.openai.com/api-keys) | ⚡ Fast (~5s) | ⭐⭐⭐ Excellent |
| 🏠 Ollama (local) | Install from [ollama.ai](https://ollama.ai), then `ollama pull phi3:mini` | 🐢 Slow (~60s) | ⭐⭐ Good |
| 🎭 Mock mode | Leave API key empty | ⚡ Instant | ⭐ Basic |

---

## 📖 Step 6: Start the Application

### 6.1 Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

**✅ Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 6.2 Test the Health Endpoint

Open a new terminal (keep the server running) and run:

```bash
curl http://localhost:8000/health
```

Or open http://localhost:8000/health in your browser.

**✅ Expected Output:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "openai": "connected",
    "search": "connected"
  }
}
```

### 6.3 Test a Query

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "When is trash pickup?"}'
```

**✅ Expected Output (abbreviated):**
```json
{
  "id": "...",
  "answer": "Trash pickup occurs every Monday and Thursday for most neighborhoods...",
  "citations": [...],
  "intent": {
    "category": "schedule",
    "confidence": 0.95
  },
  "latency_ms": 5000
}
```

---

## 📖 Step 7: Explore the Project Structure

### 7.1 Key Files and Folders

```
📦 civicnav/
├── 🐍 app/                    # Main application code
│   ├── main.py               # ⚡ FastAPI app & endpoints
│   ├── config.py             # ⚙️ Settings & environment vars
│   ├── 🤖 agents/            # AI Agent pipeline
│   │   ├── base.py          # Abstract base class
│   │   ├── query_agent.py   # 🔍 Classifies user intent
│   │   ├── retrieve_agent.py # 📚 Searches knowledge base
│   │   └── answer_agent.py  # 💬 Generates response
│   ├── 🔧 tools/            # Service integrations
│   │   ├── openai_tool.py   # 🧠 LLM client
│   │   └── search_tool.py   # 🔎 Search client
│   └── 📊 models/           # Data schemas
│       └── schemas.py       # Pydantic models
├── 📚 data/                  # Knowledge base
│   └── knowledge_base.json  # City services data
├── 📄 .env.example          # Environment template
├── 📄 requirements.txt      # Python dependencies
└── 📄 README.md             # Project documentation
```

### 7.2 Open in VS Code

```bash
code .
```

Take a moment to explore:
- Open `app/main.py` - this is where API endpoints are defined
- Open `app/agents/` folder - these are the AI agents
- Open `data/knowledge_base.json` - this is the city services data

---

## ✅ Validation Checklist

Before proceeding to the next exercise, verify:

| # | Check | Command | Expected Result |
|---|-------|---------|-----------------|
| 1 | Python version | `python --version` | 3.11+ |
| 2 | Virtual env active | Look at prompt | `(.venv)` prefix |
| 3 | Dependencies installed | `pip list \| grep fastapi` | fastapi 0.115.x |
| 4 | Server running | Check terminal | "Application startup complete" |
| 5 | Health check | `curl localhost:8000/health` | `"status": "healthy"` |
| 6 | Query works | Test with curl | Returns answer with citations |

---

## 🔧 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'app'"

**Cause:** Running from wrong directory or virtual env not activated.

**Solution:**
```bash
cd civicnav
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### ❌ "Connection refused" on localhost:8000

**Cause:** Server not running.

**Solution:** Start the server in a terminal:
```bash
uvicorn app.main:app --reload --port 8000
```

### ❌ "OpenAI API error: Invalid API key"

**Cause:** API key missing or incorrect in `.env`.

**Solution:**
1. Check `.env` has `OPENAI_API_KEY=sk-...`
2. Restart the server after editing `.env`

### ❌ Slow responses (60+ seconds)

**Cause:** Using Ollama with CPU-only inference.

**Solution:** Switch to OpenAI API in `.env`:
```env
USE_OPENAI=true
USE_OLLAMA=false
```

---

## 🎉 Congratulations!

You've completed the environment setup! Your CivicNav application is now running locally.

**📊 Progress:**
```
[====================] Exercise 0 Complete!
```

**⏭️ Next:** [Exercise 1: Understanding AI Agents & RAG](./01-understanding-agents-rag.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🛠️ Exercise 0: Environment Setup v1.0.0**

</div>
