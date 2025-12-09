# 📝 Exercise 3: Spec-Driven Development

> ⏱️ **Duration**: 20 minutes | 🎯 **Difficulty**: ⭐ Beginner | 📋 **Prerequisites**: Exercise 0-2 Complete

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | Document Version |
| ![Updated](https://img.shields.io/badge/updated-2024--12--09-green) | Last Updated |
| ![Type](https://img.shields.io/badge/type-code--generation-yellow) | Exercise Type |

---

## 🎯 Learning Objectives

By the end of this exercise, you will:

| # | Objective | Status |
|---|-----------|--------|
| 1 | 📄 Understand the SPEC.md file and its purpose | ⬜ |
| 2 | 🤖 Use Copilot to understand project architecture | ⬜ |
| 3 | ✨ Generate code that follows project conventions | ⬜ |
| 4 | 🔄 Practice the spec-driven development workflow | ⬜ |

---

## 📖 Part 1: What is Spec-Driven Development?

### 🤔 The Problem

When working with AI coding assistants, you often get:
- Code that doesn't match your project style
- Components that don't integrate with existing code
- Missing error handling or validation
- Inconsistent naming conventions

### 💡 The Solution: Specification Files

**Spec-driven development** means:
1. Write a **specification document** describing your system
2. AI assistants read the spec to understand context
3. Generated code follows the documented patterns

```
┌─────────────────────────────────────────────────────────────────┐
│              📝 Spec-Driven Development Flow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌────────────┐         ┌────────────┐         ┌────────────┐ │
│   │ 📄 SPEC.md │  read   │ 🤖 AI      │ generate│ 🐍 Code    │ │
│   │            │────────▶│  Assistant │────────▶│  Output    │ │
│   │ • Schema   │         │            │         │ (matches   │ │
│   │ • Patterns │         │            │         │  patterns) │ │
│   │ • Examples │         │            │         │            │ │
│   └────────────┘         └────────────┘         └────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Part 2: Explore the SPEC.md File

### 2.1 Open SPEC.md

In VS Code, open `SPEC.md` at the project root.

### 2.2 Key Sections to Understand

| Section | Purpose | Look For |
|---------|---------|----------|
| **Overview** | What the system does | Business goals, user personas |
| **Architecture** | System structure | Component diagram, data flow |
| **Data Models** | Schema definitions | Pydantic models, field types |
| **API Endpoints** | REST interface | Routes, request/response shapes |
| **Agent Pipeline** | AI agent design | Agent roles, inputs/outputs |

### 2.3 Read the Architecture Section

Find the section describing the three-agent pipeline:

```markdown
## Agent Pipeline

The agentic RAG pipeline consists of three specialized agents:

1. **QueryAgent**: Classifies user intent and extracts entities
2. **RetrieveAgent**: Performs hybrid search on knowledge base
3. **AnswerAgent**: Synthesizes response with citations
```

### 2.4 Find the Data Model Definitions

Look for the schemas section:

```markdown
## Data Models

### IntentClassification
- category: Category enum (schedule, permit, event, report, emergency, general)
- confidence: float (0.0 - 1.0)
- entities: list[Entity]

### SearchResult
- id: str
- title: str
- content: str
- category: Category
- relevance_score: float
```

---

## 📖 Part 3: Use Copilot to Understand the Project

### 3.1 Ask Copilot About Architecture

Open Copilot Chat and try these prompts:

**Prompt 1: Overall Understanding**
```
Look at SPEC.md and explain the CivicNav architecture in simple terms.
What are the main components and how do they work together?
```

**Prompt 2: Agent Details**
```
Based on SPEC.md, explain what each agent does:
1. QueryAgent
2. RetrieveAgent
3. AnswerAgent
Include their inputs and outputs.
```

**Prompt 3: Data Flow**
```
Using SPEC.md, trace what happens when a user asks "When is trash pickup?"
Walk through each step of the pipeline.
```

### 3.2 Compare Spec to Implementation

Ask Copilot to verify the code matches the spec:

```
Compare the SPEC.md with the actual implementation in app/agents/.
Are there any differences between what's specified and what's implemented?
```

---

## 📖 Part 4: Generate Code Following Patterns

### 4.1 Identify Project Patterns

First, let's understand the existing patterns. Open `app/agents/query_agent.py` and notice:

| Pattern | Example |
|---------|---------|
| **Type hints** | `def run(self, input_data: str) -> AgentResult:` |
| **Docstrings** | Triple-quoted description at start of functions |
| **Logging** | `logger.info(f"QueryAgent processing: ...")` |
| **Error handling** | try/except blocks with fallback behavior |
| **Return types** | `AgentResult` wrapper for outputs |

### 4.2 Generate a New Agent

Let's create a new agent that follows these patterns. Ask Copilot:

```
Looking at the patterns in app/agents/query_agent.py and following
SPEC.md conventions, create a new ValidationAgent that:

1. Takes an IntentClassification as input
2. Validates that the confidence score is above 0.5
3. Validates that the category is valid
4. Returns a ValidationResult with is_valid: bool and errors: list[str]

Follow the same patterns for:
- Type hints
- Docstrings
- Logging
- Error handling
- Return type (AgentResult wrapper)
```

### 4.3 Review the Generated Code

Copilot should generate something like:

```python
"""ValidationAgent for validating intent classifications.

This agent validates IntentClassification results before
they are passed to the retrieval stage.
"""

import logging
from typing import List

from app.agents.base import BaseAgent
from app.models.schemas import AgentResult, IntentClassification

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of validation."""
    def __init__(self, is_valid: bool, errors: List[str]):
        self.is_valid = is_valid
        self.errors = errors


class ValidationAgent(BaseAgent[IntentClassification, ValidationResult]):
    """Agent for validating intent classifications.

    Takes an IntentClassification and validates:
    - Confidence score is above threshold
    - Category is valid
    """

    CONFIDENCE_THRESHOLD = 0.5

    def __init__(self) -> None:
        """Initialize the ValidationAgent."""
        super().__init__("ValidationAgent")

    async def run(self, input_data: IntentClassification) -> AgentResult:
        """Validate the intent classification.

        Args:
            input_data: The IntentClassification to validate

        Returns:
            AgentResult containing ValidationResult
        """
        logger.info(f"ValidationAgent processing classification: {input_data.category}")

        errors: List[str] = []

        # Validate confidence
        if input_data.confidence < self.CONFIDENCE_THRESHOLD:
            errors.append(
                f"Confidence {input_data.confidence:.2f} below threshold {self.CONFIDENCE_THRESHOLD}"
            )
            logger.warning(f"Low confidence: {input_data.confidence}")

        # Validate category (already enforced by enum, but demonstrate pattern)
        try:
            _ = input_data.category.value
        except AttributeError:
            errors.append(f"Invalid category: {input_data.category}")
            logger.error(f"Invalid category: {input_data.category}")

        is_valid = len(errors) == 0

        if is_valid:
            logger.info("Validation passed")
        else:
            logger.warning(f"Validation failed with {len(errors)} errors")

        return AgentResult(
            output=ValidationResult(is_valid=is_valid, errors=errors),
            reasoning=f"Validated classification. Valid: {is_valid}, Errors: {len(errors)}",
            tools_used=self.tools_used,
        )
```

### 4.4 Verify It Matches Patterns

Check that the generated code:

| Requirement | ✅ Check |
|-------------|----------|
| Has type hints on all methods | ⬜ |
| Has docstrings | ⬜ |
| Uses logging | ⬜ |
| Has error handling | ⬜ |
| Returns AgentResult | ⬜ |
| Follows naming conventions | ⬜ |

---

## 🧪 Hands-On Exercise

### Task: Generate a New Pydantic Model

1. **Read the existing models** in `app/models/schemas.py`

2. **Notice the patterns:**
   - Field descriptions
   - Default values
   - Validators
   - Example configurations

3. **Ask Copilot to generate a new model:**

```
Looking at app/models/schemas.py patterns, create a new FeedbackRequest model for
the /api/feedback endpoint that includes:

- query_id: str (UUID of the original query)
- rating: int (1-5 star rating)
- helpful: bool (was the answer helpful)
- comment: Optional[str] (user's feedback comment, max 500 chars)

Follow the same patterns for:
- Field descriptions
- Validators
- Default values
```

4. **Review the output** and verify it matches existing patterns.

---

## ✅ Validation Checklist

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Read SPEC.md | Can explain the 3-agent architecture |
| 2 | Used Copilot to understand code | Got meaningful explanations |
| 3 | Generated code follows patterns | New code matches existing style |
| 4 | Understand spec-driven workflow | Can explain why specs help AI |

---

## 📚 Key Concepts

| Term | Definition |
|------|------------|
| **SPEC.md** | Specification document describing system architecture and patterns |
| **Spec-Driven Development** | Using specs to guide AI code generation |
| **Project Patterns** | Consistent coding conventions used throughout a project |
| **Context Window** | The text an AI can "see" when generating code |

---

## 💡 Pro Tips

### Tip 1: Include Spec in Prompts
```
Following the patterns in SPEC.md and app/agents/query_agent.py, ...
```

### Tip 2: Ask for Pattern Verification
```
Does this code follow all the patterns in SPEC.md? What's missing?
```

### Tip 3: Use Copilot Instructions
The file `.github/copilot-instructions.md` contains project-specific guidance for Copilot.

---

## 🎉 Congratulations!

You've learned spec-driven development! You can now use specifications to guide AI code generation.

**📊 Progress:**
```
[============--------] 40% Complete (Exercise 3 of 7)
```

**⏭️ Next:** [Exercise 4: Build RAG Pipeline](./04-build-rag-pipeline.md)

---

## 📋 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-09 | ✨ Initial release |

---

<div align="center">

**📝 Exercise 3: Spec-Driven Development v1.0.0**

</div>
