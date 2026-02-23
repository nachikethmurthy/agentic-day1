# Agentic Day 1 – Context Failure → Context Fix

This repo is the **starter structure** for the Day 1 assignment of the Agentic AI Enterprise Mastery Bootcamp.

The goal is to **see how naïve, stateless LLM calls can break context**, and how using a **message-based API** fixes that behavior in a way that is suitable for production systems.

---

## Project Structure

```text
agentic-day1/
├── .gitignore
├── requirements.txt
├── README.md
└── app.py
```

You should only have **one Python file**, `app.py`.

---

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root for your API keys, for example:

```bash
OPENAI_API_KEY="sk-..."
# or
GOOGLE_API_KEY="..."
```

> **Important:** `.env` is listed in `.gitignore` and **must not be committed**. Never push API keys or secrets to GitHub.

---

## Running the app

Once dependencies are installed and your `.env` is set up, run:

```bash
python app.py
```

The script will:

- Demonstrate a **context break** using naïve, stateless `llm.invoke("...")` calls
- Then demonstrate a **context fix** using `SystemMessage` and `HumanMessage` in a `messages` list and calling `llm.invoke(messages)`
- Include a reflection block at the bottom of `app.py` where you explain:
  - Why string-based invocation can fail
  - Why message-based invocation works better
  - What would break in a production AI system if we ignore message history

---

## Submission Rules (Summary)

- Repository should be **public**
- `.env` must **not** be committed
- Default branch should be `main`
- Code must run via:

```bash
python app.py
```

Please read the full assignment brief for detailed requirements and reflection prompts.

