# AI Software Engineering Assistant

A lightweight multi-agent software engineering assistant built using the **OpenAI Agents SDK**, **Google Gemini 2.5 Flash**, and Python.

The system uses five specialised AI agents to analyse requirements, generate code, test the solution, review the code, and create documentation.

---

## Project Overview

Software development involves multiple stages such as requirements analysis, coding, testing, code review, and documentation.

This project divides these tasks among specialised AI agents and coordinates them through a sequential workflow.

### Workflow

```text
User Request
     ↓
Requirements Analysis Agent
     ↓
Coding Assistant
     ↓
Testing Agent
     ↓
Code Reviewer
     ↓
Human Approval
     ↓
Documentation Writer
     ↓
Final Output
```

---

## Problem Statement

Developers often spend time performing repetitive software engineering activities such as understanding requirements, writing code, testing implementations, reviewing code, and preparing documentation.

This project demonstrates how a multi-agent AI system can divide these activities into specialised tasks and coordinate their outputs.

---

## Objectives

* Analyse software requirements automatically.
* Generate Python code from user requirements.
* Test generated code.
* Review generated code for quality and correctness.
* Provide a human approval checkpoint.
* Generate technical documentation automatically.
* Maintain shared context between workflow stages.
* Demonstrate multi-agent collaboration using the OpenAI Agents SDK.

---

## Multi-Agent System

The system contains five specialised AI agents.

### 1. Requirements Analysis Agent

Analyses the user's software request and identifies:

* Programming language
* Main task
* Inputs
* Outputs
* Important requirements
* Edge cases

### 2. Coding Assistant

Generates clean and beginner-friendly Python code based on the identified requirements.

**Tool Used:** File Writer

### 3. Testing Agent

Tests the generated Python solution and checks:

* Normal inputs
* Edge cases
* Possible errors
* Expected outputs

**Tool Used:** Python Executor

### 4. Code Reviewer

Reviews the generated code for:

* Correctness
* Requirement compliance
* Readability
* Possible bugs
* Edge cases
* Unnecessary complexity

The reviewer provides either:

`PASS`

or

`NEEDS_CHANGES`

**Tool Used:** File Reader

### 5. Documentation Writer

Generates technical documentation containing:

* Project description
* Features
* How the project works
* How to run it
* Example input/output

**Tool Used:** File Writer

---

## Tools

The project contains five function tools.

| Tool            | Purpose                                  |
| --------------- | ---------------------------------------- |
| Calculator      | Performs basic mathematical calculations |
| Python Executor | Executes Python code                     |
| File Reader     | Reads Python/text files                  |
| File Writer     | Creates or overwrites files              |
| GitHub Tool     | Provides prototype repository operations |

### GitHub Tool

The current GitHub tool is a **prototype/simulated integration**.

It provides basic responses for:

* Repository information
* Issues
* Repository status

It does not currently make live GitHub API requests.

---

## Shared Project Memory

The system maintains shared project memory using a Python dictionary.

```python
project_memory = {
    "user_request": "",
    "requirements": "",
    "code": "",
    "test_results": "",
    "code_review": "",
    "documentation": ""
}
```

The output from each stage is stored and passed as context to later stages.

---

## Agent Handoff Flow

The system uses sequential agent orchestration:

```text
User Request
     ↓
Requirements
     ↓
Generated Code
     ↓
Test Results
     ↓
Code Review
     ↓
Human Approval
     ↓
Documentation
     ↓
Final Output
```

Each stage receives information produced by the previous stages.

---

## Human Approval

After the Code Reviewer completes its review, the system asks the user:

```text
Do you approve this code? (yes/no):
```

If the user enters **yes**, the workflow continues to the Documentation Writer.

If the user does not approve the solution, the workflow stops.

This provides a human-in-the-loop control mechanism.

---

## AI Model

The project uses:

**Google Gemini 2.5 Flash**

The Gemini model is accessed through an OpenAI-compatible endpoint using:

* AsyncOpenAI
* OpenAIChatCompletionsModel
* OpenAI Agents SDK

The Gemini API key is retrieved securely from Google Colab userdata.

---

## Technology Stack

* Python
* OpenAI Agents SDK
* Google Gemini 2.5 Flash
* AsyncOpenAI
* Google Colab
* Python Function Tools

---

## Project Structure

```text
AI-Software-Engineering-Assistant/
│
├── README.md
├── ai_software_engineering_assistant.py
├── prime_checker.py
└── architecture.png
```

### Files

**ai_software_engineering_assistant.py**
Main multi-agent application.

**prime_checker.py**
Python program generated during the demonstration.

**architecture.png**
System architecture diagram.

**README.md**
Project documentation.

---

## Installation

Install the OpenAI Agents SDK:

```bash
pip install openai-agents
```

The project was developed and tested using Google Colab.

---

## Gemini API Setup

The project expects a Gemini API key to be stored in Google Colab userdata.

The code retrieves the key using:

```python
GEMINI_API_KEY = userdata.get("GEMINI_API_KEY")
```

The API key should not be hard-coded or uploaded to GitHub.

---

## Running the Project

After installing the required package and configuring the Gemini API key, run the project in Google Colab.

The demonstration request is:

```text
Create a Python program that checks whether a number is prime.

The program should:
1. Accept an integer from the user.
2. Check whether the number is prime.
3. Display whether the number is prime or not.
4. Handle numbers less than 2 correctly.
```

The workflow is started using:

```python
final_result = await run_software_engineering_assistant(
    user_request
)
```

---

## Demonstration

The example project creates a Python program that checks whether a number is prime.

The request passes through all five agents:

```text
Requirements Analysis
        ↓
Code Generation
        ↓
Testing
        ↓
Code Review
        ↓
Human Approval
        ↓
Documentation
```

The generated Python program is saved as:

```text
prime_checker.py
```

---

## Error Handling

Basic error handling is included in the tools.

### Calculator

Handles invalid mathematical expressions.

### Python Executor

Catches Python execution errors.

### File Reader

Handles file-reading errors.

### File Writer

Handles file-writing errors.

### Human Approval

Stops the workflow if the solution is rejected.

---

## Key Features

* 5 specialised AI agents
* 5 function tools
* Gemini 2.5 Flash integration
* Sequential agent orchestration
* Agent-to-agent context passing
* Shared project memory
* Automated code generation
* Testing assistance
* Automated code review
* Human approval
* Automated documentation
* Basic error handling
* Python file generation

---

## Limitations

The current implementation is intentionally lightweight.

It does not currently include:

* Persistent long-term memory
* RAG
* Database storage
* Parallel agent execution
* Live GitHub API integration
* Multi-modal inputs
* Session persistence
* Advanced autonomous planning

---

## Future Enhancements

Possible future improvements include:

1. Live GitHub API integration.
2. Persistent project memory.
3. RAG-based project knowledge retrieval.
4. Advanced automated testing.
5. Parallel agent execution.
6. Automatic code correction after failed tests.
7. GitHub pull-request automation.
8. Advanced error recovery.

---

## Architecture

The system follows a sequential multi-agent architecture:

```text
                         USER
                           │
                           ▼
              ┌─────────────────────────┐
              │ Requirements Analysis   │
              │          Agent          │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │    Coding Assistant     │
              │          Agent          │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │      Testing Agent      │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │      Code Reviewer      │
              │          Agent          │
              └────────────┬────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │ Human Approval │
                  └───────┬────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │ Documentation Writer    │
              │          Agent          │
              └────────────┬────────────┘
                           │
                           ▼
                      FINAL OUTPUT
```

---

## Conclusion

The **AI Software Engineering Assistant** demonstrates how specialised AI agents can collaborate to automate different stages of software development.

The project combines five specialised agents, five tools, shared project context, sequential agent handoffs, and human approval into a simple software engineering workflow.

The system provides a foundation that can be extended with live GitHub integration, persistent memory, RAG, parallel execution, and automated bug fixing.

---

## Project Information

**Project:** AI Software Engineering Assistant
**Domain:** Software Development
**Framework:** OpenAI Agents SDK
**AI Model:** Google Gemini 2.5 Flash
**Language:** Python
**Environment:** Google Colab
