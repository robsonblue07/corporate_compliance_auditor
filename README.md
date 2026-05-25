# Corporate Compliance Auditor: Multi-Agent AI Workflow 

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![LangChain](https://img.shields.io/badge/LangChain-LLM-green)

## 📌 Project Overview
The **Corporate Compliance Auditor** is an intelligent, multi-agent workflow designed to automate the auditing of corporate documents and contracts. Built with **LangGraph** and state-driven architecture, this system extracts critical entities from unstructured text, evaluates them against strict corporate compliance policies, and autonomously routes problematic documents to a human reviewer.

This project demonstrates advanced AI Agentic Design Patterns, specifically focusing on **Separation of Concerns**, **State Management**, and **Human-in-the-Loop (HITL)** routing for enterprise-grade applications.

## 🏗️ Architecture Design
The core workflow is orchestrated as a state machine where different AI nodes interact with a shared `AuditorState`.

1. **Document Extractor Node:** Ingests raw document text and structures key entities (e.g., Company Name, Contract Value, Governing Law).
2. **Compliance Auditor Node:** Evaluates the structured data against predefined business rules (e.g., verifying if high-value contracts include a governing law clause).
3. **Conditional Router:** Acts as the decision engine. If compliance violations are detected, the graph natively pauses execution and routes the state to a `Human-in-the-Loop` node for manual review. Otherwise, it approves the document.

## 📂 Project Structure
The repository follows a modular layout for scalability and maintainability:

```text
corporate_compliance_auditor/
├── src/
│   ├── state.py                 # Defines AuditorState and TypedDicts
│   ├── graph.py                 # StateGraph orchestration, edges, and compilation
│   ├── nodes/
│   │   ├── extractor_node.py    # Logic for entity extraction
│   │   └── auditor_node.py      # Logic for rule validation and issue logging
│   └── utils/                   # Helper modules and text parsers
├── tests/                       # Unit testing
├── requirements.txt             # Dependencies
└── README.md