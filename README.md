# Agentic Day 2 – Routing with LangGraph

This repo is the **reference solution** / **starter structure** for the Day 2 assignment of the Agentic AI Enterprise Mastery Bootcamp.

The goal is to build a **minimal LangGraph workflow** that:

- Tracks state in a typed `SupportState`
- Routes users to different paths based on `user_tier`
- Makes routing logic explicit and testable

---

## Project Structure

```text
agentic-day2-routing/
├── .gitignore
├── requirements.txt
├── README.md
└── app.py
```

You should only have **one Python file**, `app.py`, in your own submission.

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

3. Create a `.env` file in the project root for your API keys (if you use OpenAI, etc.):

```bash
OPENAI_API_KEY="sk-..."
```

> **Important:** `.env` is listed in `.gitignore` and **must not be committed**.  
> Never push API keys or secrets to GitHub.

---

## Running the app

Once dependencies are installed and your `.env` is set up (if needed), run:

```bash
python app.py
```

The script will:

- Build a `SupportState` TypedDict with `user_tier` and `should_escalate`
- Build a `StateGraph` with:
  - A `check_tier` node to decide VIP vs standard
  - A `vip_agent` node
  - A `standard_agent` node
  - A `route_by_tier` function wired via `add_conditional_edges`
- Invoke the graph twice:
  - Once with a VIP-style message
  - Once with a standard message
- Print out the resulting `user_tier` and `should_escalate` values so you can see routing behavior

---

## Submission Rules (Summary)

- Repository should be **public**
- `.env` must **not** be committed
- Default branch should be `main`
- Code must run via:

```bash
python app.py
```

Please read the full Day 2 assignment brief for detailed requirements and grading criteria.

