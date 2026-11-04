DAY 1 — AI FOR DEVOPS LEARNING JOURNEY Project: Docker Build
Troubleshooting Assistant Environment: Linux/Ubuntu shell (path shown:
/home/ubuntu/ai-devops-day1) Language: Python AI provider: OpenAI API

1.  SCENARIO / TASK Build a beginner-friendly AI-powered application
    that reads a Docker build log, sends it to an AI model, and returns
    a troubleshooting report with:

-   Error summary
-   Likely root cause
-   Recommended fix
-   Verification steps

Sample incident log: Step 3/5 : COPY requirements.txt . COPY failed:
file not found in build context

2.  CONCEPTS COVERED

-   Python functions and reading a file
-   Calling an LLM through an API
-   System and user message roles
-   System prompts and response structure
-   Docker build context and COPY errors
-   Environment variables for API keys
-   Token usage and log truncation
-   Difference between an AI-powered script and an AI agent

3.  PROJECT SETUP COMMANDS Commands used to create the project and
    virtual environment: mkdir ai-devops-day1 cd ai-devops-day1 python3
    -m venv .venv source .venv/bin/activate python -m pip install openai

Note: These commands assume a Linux/macOS shell. The traceback showed
the project running from /home/ubuntu/ai-devops-day1.

4.  FILES CREATED docker_agent.py — Python application build.log —
    sample Docker build error log .gitignore — excludes environment and
    Python cache files

Suggested .gitignore contents: .venv/ .env pycache/

5.  OPENAI SDK INSTALLATION TROUBLESHOOTING Initial issue: The script
    failed while importing OpenAI SDK classes.

Command used to check installation: python -m pip show openai

Output: Package not found: openai

Fix: python -m pip install openai

Then verify: python -m pip show openai

Import test: python -c “from openai import OpenAI, APIError,
APIConnectionError, AuthenticationError, RateLimitError; print(‘Imports
successful’)”

Important: Install the package in the same Python environment used to
run the script.

6.  API KEY CONFIGURATION The application reads the key from the
    OPENAI_API_KEY environment variable. Do not hardcode the key or
    commit it to GitHub.

Example for the current terminal session: export
OPENAI_API_KEY=“your-api-key”

The OpenAI API key and API billing are separate from a ChatGPT
subscription.

7.  IMPORTANT CODE CONCEPTS Example API request pattern used: response =
    client.chat.completions.create( model=MODEL, messages=[ {“role”:
    “system”, “content”: SYSTEM_PROMPT}, {“role”: “user”, “content”:
    f”Here is the Docker build log:“}, ], temperature=0.2, )

Role meanings: - system: instructions that define the assistant’s role
and behavior. - user: the task-specific input, in this case the Docker
build log.

String formatting: - means a newline. - creates a blank line. -
{log_text} inserts the value of the Python variable into the f-string.

SYSTEM_PROMPT: A Python variable defined in the application. It is not
automatically provided by OpenAI. It contains instructions such as
acting as a DevOps troubleshooting assistant, identifying the error,
explaining the likely cause, recommending a fix, and giving verification
steps.

Temperature: A lower value such as 0.2 generally encourages more focused
and less varied responses, but it does not guarantee correctness.

8.  LOG TRUNCATION The application reads the log. If the log exceeds
    1,500 characters, it sends only the last 1,500 characters to reduce
    input size and potentially reduce token usage.

Caution: The root cause may appear earlier in the log. Truncating only
the end can omit useful context. A production version should filter logs
more carefully or select relevant sections.

9.  QUESTIONS DISCUSSED AND ANSWERS Q: What are system and user roles?
    A: System provides behavior/instructions; user provides the actual
    request or data to analyze.

Q: What does mean? A: Two newline characters create a blank line, and
the f-string inserts the log_text variable.

Q: Where does SYSTEM_PROMPT come from? A: It is a variable you define in
your own Python code.

Q: Is the Day 1 project an AI agent? A: It is best described as an
AI-powered script/basic AI application. It follows a fixed workflow:
read log, call model, print response. A more capable agent can select
tools, inspect results, and adapt its next steps.

Q: What is the difference between an AI-powered script and an AI agent?
A: A script generally follows a predefined sequence; an agent can use
tools and make decisions about what to do next based on results.

Q: How do we search for a word in Linux? A: In a pager such as less,
press /, type the word, and press Enter; use n for next, N for previous,
q to quit. To search a file directly, use grep -n “WORD” filename.

10. DAY 1 COMPLETION Completed: The application was able to analyze the
    Docker build log and return a likely root cause and fix.

Main learning: An AI model performs the analysis, but the Python
application controls the workflow. This first project establishes the
API connection and troubleshooting pattern needed for later tool-using
agents.

END OF DAY 1 NOTES
