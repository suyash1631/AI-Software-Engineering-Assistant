# AI SOFTWARE ENGINEERING ASSISTANT
# Multi-Agent System using OpenAI Agents SDK + Gemini

# Install dependency in Colab if needed:
# !pip install -U openai-agents

import nest_asyncio
from google.colab import userdata
from openai import AsyncOpenAI

from agents import (
    Agent,
    Runner,
    function_tool,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)

nest_asyncio.apply()

# ============================================================
# 1. GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = userdata.get("GEMINI_API_KEY")

gemini_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(True)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=gemini_client,
)

# ============================================================
# 2. SHARED PROJECT MEMORY
# ============================================================

project_memory = {
    "user_request": "",
    "requirements": "",
    "code": "",
    "test_results": "",
    "code_review": "",
    "documentation": "",
}

# ============================================================
# 3. TOOLS
# ============================================================

@function_tool
def calculator(expression: str) -> str:
    """Performs a basic mathematical calculation."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Error: Invalid mathematical expression."


@function_tool
def python_executor(code: str) -> str:
    """Executes Python code and reports the result."""
    try:
        exec(code, {"__builtins__": __builtins__}, {})
        return "Code executed successfully."
    except Exception as e:
        return f"Code execution error: {e}"


@function_tool
def file_reader(filename: str) -> str:
    """Reads a text or Python file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


@function_tool
def file_writer(filename: str, content: str) -> str:
    """Creates or overwrites a file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Error writing file: {e}"


@function_tool
def github_tool(action: str, repository: str = "") -> str:
    """Prototype GitHub integration tool."""
    if action.lower() == "repository":
        return f"Repository information requested for: {repository}"
    if action.lower() == "issues":
        return f"GitHub issues requested for: {repository}"
    if action.lower() == "status":
        return f"Repository status requested for: {repository}"
    return "Unknown GitHub action."


# ============================================================
# 4. FIVE SPECIALISED AGENTS
# ============================================================

requirements_agent = Agent(
    name="Requirements Analysis Agent",
    instructions="""
    You are a requirements analysis specialist.
    Identify:
    1. Programming language
    2. Main task
    3. Inputs
    4. Outputs
    5. Requirements
    6. Edge cases
    Keep the response simple and concise.
    """,
    model=gemini_model,
)

coding_agent = Agent(
    name="Coding Assistant",
    instructions="""
    You are an expert Python developer.
    Generate clean, beginner-friendly Python code based on
    the requirements provided. Follow all requirements,
    avoid unnecessary complexity, and include comments.
    """,
    model=gemini_model,
    tools=[file_writer],
)

testing_agent = Agent(
    name="Testing Agent",
    instructions="""
    You are a software testing specialist.
    Test generated Python code using normal inputs and edge cases.
    Report errors, expected behavior, and whether the code works.
    """,
    model=gemini_model,
    tools=[python_executor],
)

reviewer_agent = Agent(
    name="Code Reviewer",
    instructions="""
    You are an experienced code reviewer.
    Review code for correctness, requirement compliance,
    readability, bugs, and edge cases.
    Give PASS or NEEDS_CHANGES and explain briefly.
    """,
    model=gemini_model,
    tools=[file_reader],
)

documentation_agent = Agent(
    name="Documentation Writer",
    instructions="""
    You are a technical documentation specialist.
    Create concise documentation with:
    project title, description, features, workflow,
    setup/run instructions, and example input/output.
    """,
    model=gemini_model,
    tools=[file_writer],
)

# ============================================================
# 5. MAIN MULTI-AGENT WORKFLOW
# ============================================================

async def run_software_engineering_assistant(user_request: str):
    print("=" * 70)
    print("       AI SOFTWARE ENGINEERING ASSISTANT")
    print("=" * 70)

    project_memory["user_request"] = user_request

    # Agent 1: Requirements
    print("\n[1/5] Requirements Analysis Agent")
    result = await Runner.run(requirements_agent, user_request)
    requirements_output = result.final_output
    project_memory["requirements"] = requirements_output
    print(requirements_output)

    # Agent 2: Coding
    print("\n[2/5] Coding Assistant")
    coding_input = f"""
    User Request:
    {user_request}

    Requirements:
    {requirements_output}

    Generate the required Python program.
    """
    result = await Runner.run(coding_agent, coding_input)
    code_output = result.final_output
    project_memory["code"] = code_output
    print(code_output)

    # Agent 3: Testing
    print("\n[3/5] Testing Agent")
    testing_input = f"""
    User Request:
    {user_request}

    Generated Code:
    {code_output}

    Test the code with normal inputs and edge cases.
    Report whether it works correctly.
    """
    result = await Runner.run(testing_agent, testing_input)
    testing_output = result.final_output
    project_memory["test_results"] = testing_output
    print(testing_output)

    # Agent 4: Review
    print("\n[4/5] Code Reviewer")
    review_input = f"""
    User Request:
    {user_request}

    Requirements:
    {requirements_output}

    Generated Code:
    {code_output}

    Testing Results:
    {testing_output}

    Review the code and give:
    - PASS or NEEDS_CHANGES
    - Problems
    - Suggested improvements
    """
    result = await Runner.run(reviewer_agent, review_input)
    review_output = result.final_output
    project_memory["code_review"] = review_output
    print(review_output)

    # Human approval
    print("\n" + "=" * 70)
    print("                     HUMAN APPROVAL")
    print("=" * 70)

    approval = input("Do you approve this code? (yes/no): ").strip().lower()

    if approval != "yes":
        print("\nCode rejected. Workflow stopped.")
        return project_memory

    print("\nCode approved.")

    # Agent 5: Documentation
    print("\n[5/5] Documentation Writer")
    documentation_input = f"""
    Create documentation for this completed project.

    Project:
    AI Software Engineering Assistant

    User Request:
    {user_request}

    Requirements:
    {requirements_output}

    Generated Code:
    {code_output}

    Testing Results:
    {testing_output}

    Code Review:
    {review_output}

    Human Approval:
    Approved

    Include:
    - Project description
    - Features
    - How it works
    - How to run it
    - Example input/output
    """
    result = await Runner.run(documentation_agent, documentation_input)
    documentation_output = result.final_output
    project_memory["documentation"] = documentation_output
    print(documentation_output)

    # Save generated Python code
    clean_code = code_output
    if "```python" in clean_code:
        clean_code = clean_code.replace("```python", "").replace("```", "")
    elif "```" in clean_code:
        clean_code = clean_code.replace("```", "")

    with open("prime_checker.py", "w", encoding="utf-8") as f:
        f.write(clean_code.strip())

    print("\nGenerated file saved as: prime_checker.py")
    print("\nPROJECT COMPLETED")

    return project_memory


# ============================================================
# 6. RUN THE ASSIGNMENT DEMO
# ============================================================

user_request = """
Create a Python program that checks whether a number is prime.

The program should:
1. Accept an integer from the user.
2. Check whether the number is prime.
3. Display whether the number is prime or not.
4. Handle numbers less than 2 correctly.
"""

final_result = await run_software_engineering_assistant(user_request)
