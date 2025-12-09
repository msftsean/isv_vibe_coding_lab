# 🔌 Exercise 2: Azure MCP Server Setup

> ⏱️ **Duration**: 20 minutes | 🎯 **Difficulty**: ⭐ Beginner | 📋 **Prerequisites**: Exercise 0-1 Complete

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-configuration-orange) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 🔌 Understand what MCP (Model Context Protocol) is | ⬜ |
| 2 | ⚙️ Configure VS Code for Copilot Agent Mode | ⬜ |
| 3 | 🔷 Set up the Azure MCP Server | ⬜ |
| 4 | ✅ Verify Copilot can access Azure resources | ⬜ |

---

## 📖 Part 1: What is MCP?

### 🤔 The Problem

AI assistants like GitHub Copilot are powerful, but they can't:
- Access your Azure resources
- Read your databases
- Call your APIs
- Use your custom tools

### 💡 The Solution: Model Context Protocol (MCP)

**MCP** is an open protocol that lets AI assistants use external tools safely.

```
┌─────────────────────────────────────────────────────────────────┐
│                    🔌 MCP Architecture                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐         ┌─────────────┐         ┌───────────┐ │
│  │ 🤖 AI       │  MCP    │ 🔧 MCP      │  API    │ ☁️ Azure  │ │
│  │   Assistant │◀───────▶│    Server   │◀───────▶│   Services│ │
│  │ (Copilot)   │         │             │         │           │ │
│  └─────────────┘         └─────────────┘         └───────────┘ │
│                                                                  │
│  The AI asks the MCP server to perform actions,                 │
│  and the server interacts with Azure on its behalf.             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔷 Azure MCP Server

The **Azure MCP Server** gives Copilot access to:

| Tool | What it Does |
|------|--------------|
| `azure_list_subscriptions` | List your Azure subscriptions |
| `azure_list_resource_groups` | List resource groups |
| `azure_get_resource` | Get details about a resource |
| `azure_deploy_template` | Deploy ARM/Bicep templates |
| `azure_cosmos_query` | Query Cosmos DB |
| `azure_storage_list` | List storage accounts |

---

## 📖 Part 2: Configure VS Code Agent Mode

### 2.1 Open VS Code Settings

Press `Ctrl+,` (or `Cmd+,` on Mac) to open Settings.

### 2.2 Search for Agent Mode

In the search bar, type: `github.copilot.chat.agent`

### 2.3 Enable Agent Mode

Find and **check** these settings:

| Setting | Value | Purpose |
|---------|-------|---------|
| `Github › Copilot › Chat: Agent Mode` | ✅ Enabled | Allow Copilot to use tools |
| `Github › Copilot › Chat: Use Project MCP Servers` | ✅ Enabled | Use project-specific MCP servers |

**📸 Screenshot reference:**
```
┌─────────────────────────────────────────────────────────────────┐
│ ⚙️ Settings                                                     │
├─────────────────────────────────────────────────────────────────┤
│ 🔍 github.copilot.chat.agent                                    │
│                                                                  │
│ ☑️ Github › Copilot › Chat: Agent Mode                          │
│    Enable agent mode for Copilot Chat                           │
│                                                                  │
│ ☑️ Github › Copilot › Chat: Use Project MCP Servers             │
│    Use MCP servers defined in .vscode/mcp.json                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Restart VS Code

Close and reopen VS Code for settings to take effect.

---

## 📖 Part 3: Review MCP Configuration

### 3.1 Open the MCP Configuration File

In VS Code, open: `.vscode/mcp.json`

You should see:

```json
{
  "servers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"]
    }
  }
}
```

### 3.2 Understanding the Configuration

| Field | Value | Meaning |
|-------|-------|---------|
| `servers` | Object | List of MCP servers |
| `azure` | Server name | Identifier for this server |
| `command` | `npx` | Node.js package runner |
| `args` | `["-y", "@azure/mcp@latest", ...]` | Download and run Azure MCP |

This tells VS Code:
> "When Copilot needs Azure tools, run the Azure MCP server using npx"

---

## 📖 Part 4: Authenticate with Azure

### 4.1 Check Azure CLI Installation

```bash
az --version
```

**✅ Expected Output:**
```
azure-cli    2.x.x
...
```

**❌ If not installed:**
Download from [aka.ms/installazurecli](https://aka.ms/installazurecli)

### 4.2 Login to Azure

```bash
az login
```

This opens a browser window. Sign in with your Azure account.

**✅ Expected Output:**
```json
[
  {
    "cloudName": "AzureCloud",
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "isDefault": true,
    "name": "Your Subscription Name",
    "state": "Enabled",
    "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "user": {
      "name": "you@example.com",
      "type": "user"
    }
  }
]
```

### 4.3 Verify Account

```bash
az account show
```

**✅ Expected Output:**
Shows your current subscription details.

---

## 📖 Part 5: Test Azure MCP Server

### 5.1 Start the Azure MCP Server Manually (Optional Test)

You can test the server independently:

```bash
npx -y @azure/mcp@latest server start
```

**✅ Expected Output:**
```
Azure MCP Server started
Listening for connections...
```

Press `Ctrl+C` to stop.

### 5.2 Test in Copilot Chat

1. Open the **Copilot Chat** panel in VS Code (click the Copilot icon in sidebar)

2. Type this prompt:
```
@azure List my Azure subscriptions
```

**✅ Expected Response:**
Copilot should list your Azure subscriptions with their IDs and names.

### 5.3 Try More Azure Queries

| Prompt | Expected Result |
|--------|-----------------|
| `@azure List my resource groups` | Shows your resource groups |
| `@azure What Azure services do I have?` | Lists deployed resources |
| `@azure Show me my storage accounts` | Lists storage accounts |

---

## 🧪 Hands-On Exercise

### Task: Explore Azure Resources with Copilot

1. **Ask Copilot about your subscription:**
```
@azure Tell me about my Azure subscription and what resources I have
```

2. **Get specific resource details:**
```
@azure Show me the details of my resource groups
```

3. **Document what you find:**

| Resource Type | Count | Names |
|---------------|-------|-------|
| Resource Groups | ___ | _______________ |
| Storage Accounts | ___ | _______________ |
| App Services | ___ | _______________ |

---

## 🔧 Troubleshooting

### ❌ "Agent Mode not available"

**Cause:** Copilot extension not updated or feature not enabled.

**Solution:**
1. Update the GitHub Copilot extension
2. Ensure you have Copilot Chat (not just Copilot)
3. Check settings as described in Part 2

### ❌ "Could not connect to MCP server"

**Cause:** Node.js not installed or npx not available.

**Solution:**
```bash
# Check Node.js
node --version  # Should be 18+

# If not installed, get it from nodejs.org
```

### ❌ "Azure authentication failed"

**Cause:** Not logged in or token expired.

**Solution:**
```bash
# Re-authenticate
az logout
az login
```

### ❌ "@azure not recognized"

**Cause:** MCP server not configured or VS Code not restarted.

**Solution:**
1. Verify `.vscode/mcp.json` exists
2. Restart VS Code completely
3. Wait 10-15 seconds after restart for MCP to initialize

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Agent Mode enabled | Settings shows checkmarks |
| 2 | Azure CLI installed | `az --version` works |
| 3 | Logged into Azure | `az account show` shows your account |
| 4 | MCP config exists | `.vscode/mcp.json` present |
| 5 | Copilot can list resources | `@azure List subscriptions` returns data |

---

## 📚 Key Concepts

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - allows AI to use external tools |
| **Agent Mode** | VS Code feature enabling Copilot to use tools |
| **Azure MCP Server** | MCP implementation for Azure services |
| **DefaultAzureCredential** | Azure SDK's automatic authentication |

---

## 🎉 Congratulations!

You've configured the Azure MCP Server! Copilot can now interact with your Azure resources.

**📊 Progress:**
```
[==========----------] 30% Complete (Exercise 2 of 7)
```

**⏭️ Next:** [Exercise 3: Spec-Driven Development](./03-spec-driven-development.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🔌 Exercise 2: Azure MCP Server Setup v1.0.0**

</div>
