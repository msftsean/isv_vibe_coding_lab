# 🚀 Exercise 6: Deploy with Azure Developer CLI (azd)

> ⏱️ **Duration**: 35 minutes | 🎯 **Difficulty**: ⭐⭐ Intermediate | 📋 **Prerequisites**: Exercise 0-5 Complete, Azure Subscription

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-deployment-red) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 🔧 Install and configure Azure Developer CLI (azd) | ⬜ |
| 2 | 📁 Understand the azure.yaml configuration | ⬜ |
| 3 | 🚀 Deploy CivicNav to Azure Container Apps | ⬜ |
| 4 | ✅ Verify the deployed application | ⬜ |
| 5 | 🔄 Update and redeploy the application | ⬜ |

---

## 📖 Part 1: What is Azure Developer CLI?

### 1.1 The Problem with Manual Deployment

Deploying an application to Azure typically requires:
- Creating resource groups
- Provisioning services (App Service, Container Apps, etc.)
- Configuring networking
- Setting environment variables
- Building and pushing container images
- ... and many more steps!

### 1.2 The Solution: Azure Developer CLI (azd)

**azd** is a command-line tool that simplifies Azure deployments:

```
┌─────────────────────────────────────────────────────────────────┐
│              🚀 Azure Developer CLI (azd)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Without azd:                                                   │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │ az  │→│ az  │→│ az  │→│ az  │→│docker│→│ az  │→│ az  │      │
│  │group│ │acr  │ │app  │ │keyvault│ │push│ │ ... │→│deploy│    │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘      │
│     😰 Many manual steps, easy to make mistakes                 │
│                                                                  │
│  With azd:                                                      │
│  ┌─────────────────────────────────────────────────────┐        │
│  │              azd up                                  │        │
│  │     (One command does everything!)                   │        │
│  └─────────────────────────────────────────────────────┘        │
│     😊 Simple, repeatable, infrastructure as code               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Key azd Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `azd init` | Initialize a new project | First time setup |
| `azd up` | Provision and deploy everything | Full deployment |
| `azd provision` | Create Azure resources only | Infrastructure changes |
| `azd deploy` | Deploy code only | Code updates |
| `azd down` | Delete all resources | Cleanup |
| `azd env` | Manage environments | Dev/staging/prod |

---

## 📖 Part 2: Install Azure Developer CLI

### 2.1 Install azd

Choose your platform:

| Platform | Command |
|----------|---------|
| 🪟 Windows (winget) | `winget install Microsoft.Azd` |
| 🪟 Windows (PowerShell) | `powershell -ex AllSigned -c "Invoke-RestMethod 'https://aka.ms/install-azd.ps1' \| Invoke-Expression"` |
| 🍎 macOS | `brew install azure-dev` |
| 🐧 Linux | `curl -fsSL https://aka.ms/install-azd.sh \| bash` |

### 2.2 Verify Installation

```bash
azd version
```

**✅ Expected Output:**
```
azd version 1.x.x (commit xxxxxxx)
```

### 2.3 Login to Azure

```bash
azd auth login
```

This opens a browser window. Sign in with your Azure account.

**✅ Expected Output:**
```
Logged in to Azure.
```

---

## 📖 Part 3: Understand the Project Configuration

### 3.1 The azure.yaml File

Open `azure.yaml` in the project root:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json

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
```

### 3.2 Understanding the Configuration

| Field | Value | Purpose |
|-------|-------|---------|
| `name` | civicnav | Application name (used in resource naming) |
| `services.api` | Object | Defines the API service |
| `project` | `.` | Source code location |
| `language` | python | Runtime environment |
| `host` | containerapp | Azure Container Apps deployment |
| `docker.path` | Dockerfile | Container build instructions |

### 3.3 The Infrastructure Files

The `infra/` folder contains Bicep templates:

```
📦 infra/
├── 📄 main.bicep          # Main infrastructure definition
├── 📄 main.parameters.json # Parameter values
├── 📁 core/
│   ├── 📄 host/           # Container Apps config
│   ├── 📄 monitor/        # Application Insights
│   └── 📄 security/       # Key Vault
└── 📁 app/
    └── 📄 api.bicep       # API-specific resources
```

### 3.4 Examine the Dockerfile

Open `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY data/ ./data/

# Set environment variables
ENV PORT=8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📖 Part 4: Deploy to Azure

### 4.1 Initialize the Environment

```bash
azd init
```

**Prompts and responses:**

| Prompt | Response |
|--------|----------|
| "Select a template" | Select "Use code in current directory" |
| "Environment name" | Enter `dev` (or your preferred name) |

**✅ Expected Output:**
```
SUCCESS: Your project has been initialized!
```

### 4.2 Configure Environment Variables

Set the required environment variables:

```bash
# Set OpenAI API key (required for production)
azd env set OPENAI_API_KEY "sk-your-api-key-here"

# Enable OpenAI mode
azd env set USE_OPENAI "true"
azd env set USE_OLLAMA "false"
```

### 4.3 Deploy Everything with One Command

```bash
azd up
```

This single command will:
1. Create an Azure resource group
2. Provision Azure Container Apps environment
3. Set up Azure Container Registry
4. Build and push the Docker image
5. Deploy the application
6. Configure networking and environment variables

**📊 Progress Indicators:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    🚀 azd up Progress                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Packaging services                                     │
│  [████████████████████] 100%                                    │
│  ✅ api: Docker image built                                     │
│                                                                  │
│  Step 2: Provisioning Azure resources                           │
│  [████████████░░░░░░░░] 60%                                     │
│  • Creating resource group...                                   │
│  • Deploying Container Apps environment...                      │
│  • Creating Container Registry...                               │
│                                                                  │
│  Step 3: Deploying services                                     │
│  [░░░░░░░░░░░░░░░░░░░░] 0%                                      │
│  Waiting for provisioning...                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 Deployment Complete

After 5-10 minutes, you'll see:

```
SUCCESS: Your application was provisioned and deployed to Azure!

You can view the resources created under the resource group rg-civicnav in Azure Portal:
https://portal.azure.com/#@/resource/subscriptions/.../resourceGroups/rg-civicnav

Endpoint:
  api: https://civicnav-api-xxxxx.azurecontainerapps.io
```

**🎉 Save the endpoint URL!** You'll need it to test the deployment.

---

## 📖 Part 5: Verify the Deployment

### 5.1 Test the Health Endpoint

```bash
curl https://civicnav-api-xxxxx.azurecontainerapps.io/health
```

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

### 5.2 Test a Query

```bash
curl -X POST https://civicnav-api-xxxxx.azurecontainerapps.io/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "When is trash pickup?"}'
```

**✅ Expected Output:**
```json
{
  "id": "...",
  "answer": "Trash pickup occurs every Monday and Thursday...",
  "citations": [...],
  "intent": {
    "category": "schedule",
    "confidence": 0.95
  }
}
```

### 5.3 View in Azure Portal

1. Go to the Azure Portal URL from the deployment output
2. Click on the Container App resource
3. Explore:
   - **Overview**: See the app URL and status
   - **Logs**: View application logs
   - **Metrics**: See performance metrics

```
┌─────────────────────────────────────────────────────────────────┐
│              🌐 Azure Portal - Container App                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  civicnav-api                                                   │
│  ├─ Status: Running ✅                                          │
│  ├─ URL: https://civicnav-api-xxxxx.azurecontainerapps.io      │
│  ├─ Replicas: 1                                                 │
│  └─ Location: East US                                           │
│                                                                  │
│  Quick Actions:                                                 │
│  [📊 Metrics] [📜 Logs] [🔄 Restart] [📈 Scale]                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Part 6: Update and Redeploy

### 6.1 Make a Code Change

Open `app/main.py` and update the version in the health endpoint:

```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.1.0",  # Changed from 1.0.0
        ...
    }
```

### 6.2 Deploy Only Code Changes

Since infrastructure hasn't changed, use `azd deploy`:

```bash
azd deploy
```

This is faster than `azd up` because it only:
1. Rebuilds the Docker image
2. Pushes to Container Registry
3. Updates the Container App

**⏱️ Time:** ~2-3 minutes (vs 5-10 for full `azd up`)

### 6.3 Verify the Update

```bash
curl https://civicnav-api-xxxxx.azurecontainerapps.io/health | jq '.version'
```

**✅ Expected Output:**
```
"1.1.0"
```

---

## 🧪 Hands-On Exercise

### Task 1: Deploy CivicNav

1. **Initialize and deploy:**
```bash
azd init
azd env set OPENAI_API_KEY "your-api-key"
azd up
```

2. **Record the deployment details:**

| Item | Value |
|------|-------|
| Resource Group | ________________ |
| Container App URL | ________________ |
| Deployment Duration | ________________ |

### Task 2: Test the Deployed Application

1. **Run these commands** with your deployed URL:

```bash
# Health check
curl https://YOUR-URL.azurecontainerapps.io/health

# Query test
curl -X POST https://YOUR-URL.azurecontainerapps.io/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I report a pothole?"}'
```

2. **Fill in the results:**

| Test | Status | Response Time |
|------|--------|---------------|
| Health endpoint | ✅ / ❌ | _____ ms |
| Query endpoint | ✅ / ❌ | _____ ms |

### Task 3: Explore Azure Portal

1. Navigate to your resource group in Azure Portal
2. Find these resources:

| Resource Type | Name | Purpose |
|---------------|------|---------|
| Container App | ________________ | Runs the API |
| Container Registry | ________________ | Stores Docker images |
| Log Analytics | ________________ | Collects logs |

---

## 📖 Part 7: Managing Environments

### 7.1 Create Multiple Environments

azd supports multiple environments (dev, staging, prod):

```bash
# Create a staging environment
azd env new staging

# Set staging-specific variables
azd env set OPENAI_API_KEY "staging-api-key" --env staging

# Deploy to staging
azd up --env staging
```

### 7.2 Switch Between Environments

```bash
# List environments
azd env list

# Switch active environment
azd env select dev
```

### 7.3 Environment Configuration

```
┌─────────────────────────────────────────────────────────────────┐
│              🌍 Environment Management                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Environments:                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ dev (active)                                         │        │
│  │ • Resource Group: rg-civicnav-dev                   │        │
│  │ • URL: civicnav-dev-xxx.azurecontainerapps.io      │        │
│  │ • OpenAI: gpt-4o-mini                               │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ staging                                              │        │
│  │ • Resource Group: rg-civicnav-staging               │        │
│  │ • URL: civicnav-staging-xxx.azurecontainerapps.io  │        │
│  │ • OpenAI: gpt-4o                                    │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐        │
│  │ prod                                                 │        │
│  │ • Resource Group: rg-civicnav-prod                  │        │
│  │ • URL: civicnav-prod-xxx.azurecontainerapps.io     │        │
│  │ • OpenAI: gpt-4o (scaled)                           │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Part 8: Cleanup

### 8.1 Delete All Resources

When you're done, clean up to avoid charges:

```bash
azd down
```

**⚠️ Warning:** This deletes ALL resources in the environment!

**Prompts:**
```
? Total resources to delete: 5, are you sure you want to continue? (y/N) y
```

**✅ Expected Output:**
```
SUCCESS: Your application was deleted from Azure.
```

### 8.2 Verify Cleanup

```bash
# This should fail (resource deleted)
curl https://civicnav-api-xxxxx.azurecontainerapps.io/health
```

---

## 🔧 Troubleshooting

### ❌ "azd: command not found"

**Cause:** azd not installed or not in PATH.

**Solution:**
```bash
# Windows - restart terminal after install
# macOS/Linux - ensure PATH is updated
source ~/.bashrc  # or ~/.zshrc
```

### ❌ "Deployment failed: Container image not found"

**Cause:** Docker build failed.

**Solution:**
```bash
# Test Docker build locally
docker build -t civicnav .
docker run -p 8000:8000 civicnav
```

### ❌ "Error: subscription not found"

**Cause:** Not logged in or wrong subscription.

**Solution:**
```bash
azd auth logout
azd auth login
az account set --subscription "Your Subscription Name"
```

### ❌ "Application unhealthy"

**Cause:** Missing environment variables or startup errors.

**Solution:**
```bash
# Check logs
azd logs

# Verify environment variables
azd env get-values
```

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | azd installed | `azd version` shows version |
| 2 | Logged in to Azure | `azd auth login` succeeded |
| 3 | Deployed successfully | `azd up` completed |
| 4 | Health check works | `/health` returns 200 |
| 5 | Query endpoint works | `/api/query` returns answer |
| 6 | Can view in Portal | Resources visible in Azure Portal |

---

## 📚 Key Concepts

| Term | Definition |
|------|------------|
| **azd** | Azure Developer CLI - simplified deployment tool |
| **azure.yaml** | Project configuration file for azd |
| **Bicep** | Azure infrastructure as code language |
| **Container Apps** | Azure's serverless container platform |
| **Environment** | Named configuration for deployment (dev/staging/prod) |

---

## 💡 Pro Tips

### Tip 1: Use .azure Folder for Secrets
azd stores environment config in `.azure/` - add to `.gitignore`:
```
.azure/
```

### Tip 2: Preview Changes Before Deploying
```bash
azd provision --preview
```

### Tip 3: Stream Logs in Real-time
```bash
azd monitor --live
```

---

## 🎉 Congratulations!

You've deployed CivicNav to Azure! Your agentic RAG application is now running in the cloud.

**📊 Progress:**
```
[==================--] 85% Complete (Exercise 6 of 7)
```

**⏭️ Next:** [Exercise 7: Expose as MCP Server](./07-expose-as-mcp-server.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**🚀 Exercise 6: Deploy with azd v1.0.0**

</div>
