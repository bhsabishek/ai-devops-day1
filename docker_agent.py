"""
docker_agent.py - A simple AI agent that analyzes Docker build failures.

Usage:
    export OPENAI_API_KEY="sk-..."
    python docker_agent.py              # reads build.log
    python docker_agent.py other.log    # reads a different log file
"""

import os
import sys

from openai import OpenAI, APIError, APIConnectionError, AuthenticationError, RateLimitError

# Which model to use. You can override it with the OPENAI_MODEL environment variable.
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Build logs can be huge. The error is almost always near the end,
# so we only send the last part of the log to keep cost and tokens low.
MAX_LOG_CHARS = 15000

SYSTEM_PROMPT = """You are a senior DevOps troubleshooting assistant specializing in Docker.
You will be given the output of a failed `docker build`.

Analyze the log and respond in exactly this format:

## Error Summary
A one or two sentence description of what failed and at which build step.

## Likely Root Cause
Explain why the failure happened. Quote the specific log line(s) that prove it.

## Recommended Fix
Concrete steps to fix it. Include corrected Dockerfile lines or commands where helpful.

## Verification Steps
Commands the user should run to confirm the fix works.

Rules:
- Base your answer only on evidence in the log. If the log is ambiguous, say so.
- Keep the answer concise and practical for a beginner."""


def read_log(path):
    """Read the build log from disk. Returns the text, or None if it can't be read."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: log file '{path}' not found.")
        return None
    except PermissionError:
        print(f"Error: permission denied when reading '{path}'.")
        return None

    if not content.strip():
        print(f"Error: log file '{path}' is empty.")
        return None

    # Keep only the tail of very long logs.
    if len(content) > MAX_LOG_CHARS:
        print(f"Note: log is long; sending only the last {MAX_LOG_CHARS} characters.")
        content = content[-MAX_LOG_CHARS:]

    return content


def analyze_log(log_text):
    """Send the log to the OpenAI API and return the model's analysis, or None on failure."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: the OPENAI_API_KEY environment variable is not set.")
        return None

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Here is the Docker build log:\n\n{log_text}"},
            ],
            temperature=0.2,  # low temperature = more focused, consistent answers
        )
    except AuthenticationError:
        print("Error: authentication failed. Check that your OPENAI_API_KEY is valid.")
        return None
    except RateLimitError:
        print("Error: rate limit or quota exceeded. Wait a bit or check your billing.")
        return None
    except APIConnectionError:
        print("Error: could not connect to the OpenAI API. Check your network.")
        return None
    except APIError as e:
        print(f"Error: the OpenAI API returned an error: {e}")
        return None

    return response.choices[0].message.content


def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else "build.log"

    print(f"Reading {log_path}...")
    log_text = read_log(log_path)
    if log_text is None:
        sys.exit(1)

    print(f"Analyzing with {MODEL}...\n")
    analysis = analyze_log(log_text)
    if analysis is None:
        sys.exit(1)

    print(analysis)


if __name__ == "__main__":
    main()
