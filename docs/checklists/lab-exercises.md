# 📋 Lab Exercises Requirements Quality Checklist

> 🎓 Unit tests for lab exercise requirements - validating completeness, clarity, and learning objective coverage.

---

## 📊 Status

| Metric | Status |
|--------|--------|
| ![Type](https://img.shields.io/badge/type-lab--exercises-blue) | Domain |
| ![Depth](https://img.shields.io/badge/depth-quick--scan-green) | Rigor |
| ![Scope](https://img.shields.io/badge/scope-functional-yellow) | Focus |

---

## 📋 Meta

| Field | Value |
|-------|-------|
| **Purpose** | Validate lab exercise requirements quality |
| **Created** | 2024-12-09 |
| **Audience** | Author (pre-commit sanity check) |
| **Source** | docs/exercises/README.md, SPEC.md |

---

## 🎯 Learning Objectives Completeness

- [ ] **CHK001** - Are explicit learning objectives defined for each exercise? [Gap]
- [ ] **CHK002** - Is the expected skill level (beginner/intermediate/advanced) specified per exercise? [Completeness, Exercise Summary]
- [ ] **CHK003** - Are prerequisites for each exercise explicitly listed? [Gap]
- [ ] **CHK004** - Is the relationship between exercises and SPEC.md user stories documented? [Traceability, Gap]

---

## 📝 Exercise Step Clarity

- [ ] **CHK005** - Are step instructions specific enough to follow without ambiguity? [Clarity, Exercise 1-6]
- [ ] **CHK006** - Is "Enable Agent Mode" in Exercise 1 defined with specific VS Code settings path? [Clarity, Exercise 1 Step 1]
- [ ] **CHK007** - Is "generate a new model" in Exercise 2 specified with expected model type/name? [Clarity, Exercise 2 Step 3]
- [ ] **CHK008** - Are "sample queries" in Exercise 3 defined or provided? [Gap, Exercise 3 Step 4]
- [ ] **CHK009** - Is "Test end-to-end with the chat UI" specified with test scenarios? [Clarity, Exercise 4 Step 4]
- [ ] **CHK010** - Is "Verify deployment in Azure portal" defined with specific verification steps? [Clarity, Exercise 5 Step 3]

---

## ✅ Validation Criteria Measurability

- [ ] **CHK011** - Can "Copilot can respond to Azure resource queries" be objectively measured? [Measurability, Exercise 1 Validation]
- [ ] **CHK012** - Can "Generated code follows project conventions" be objectively verified? [Measurability, Exercise 2 Validation]
- [ ] **CHK013** - Is "relevant results with scores" defined with expected score ranges or thresholds? [Clarity, Exercise 3 Validation]
- [ ] **CHK014** - Is "Complete answers with citations" defined with minimum citation requirements? [Clarity, Exercise 4 Validation]
- [ ] **CHK015** - Can "Application accessible via Container Apps URL" be verified with specific test? [Measurability, Exercise 5 Validation]
- [ ] **CHK016** - Is "Copilot uses CivicNav tools successfully" defined with expected output criteria? [Clarity, Exercise 6 Validation]

---

## ⏱️ Duration Accuracy

- [ ] **CHK017** - Are duration estimates based on stated skill level (intermediate)? [Assumption]
- [ ] **CHK018** - Does total time (2.5 hours) account for setup and troubleshooting buffer? [Completeness]
- [ ] **CHK019** - Is the 45-minute RAG Pipeline exercise realistic given implementation scope? [Clarity, Exercise 3]

---

## 🔗 File Reference Accuracy

- [ ] **CHK020** - Do all referenced files exist in the repository? [Consistency]
- [ ] **CHK021** - Is `.vscode/mcp.json` referenced in Exercise 1 present and correct? [Traceability]
- [ ] **CHK022** - Is `app/tools/search_tool.py` referenced in Exercise 3 complete for the exercise? [Traceability]
- [ ] **CHK023** - Is `app/mcp/server.py` referenced in Exercise 6 documented for learners? [Traceability]

---

## 🚀 Extension Challenge Coverage

- [ ] **CHK024** - Are extension challenge requirements complete enough to implement? [Completeness, Extension Challenge]
- [ ] **CHK025** - Is "session timeout/cleanup" specified with timing requirements? [Gap, Extension Challenge]
- [ ] **CHK026** - Are success criteria defined for the extension challenge? [Gap]

---

## 📊 Exercise Progression

- [ ] **CHK027** - Is exercise ordering logical (dependencies flow correctly)? [Consistency]
- [ ] **CHK028** - Are skill build-up requirements between exercises documented? [Gap]
- [ ] **CHK029** - Is the difficulty rating (Easy/Medium/Hard) consistently applied? [Consistency, Exercise Summary]

---

## 📋 Checklist Summary

| Dimension | Items | Coverage |
|-----------|-------|----------|
| Learning Objectives | CHK001-CHK004 | 4 items |
| Step Clarity | CHK005-CHK010 | 6 items |
| Validation Measurability | CHK011-CHK016 | 6 items |
| Duration Accuracy | CHK017-CHK019 | 3 items |
| File References | CHK020-CHK023 | 4 items |
| Extension Challenge | CHK024-CHK026 | 3 items |
| Exercise Progression | CHK027-CHK029 | 3 items |
| **Total** | | **29 items** |

---

<div align="center">

**📋 Lab Exercises Checklist v1.0.0**

</div>
