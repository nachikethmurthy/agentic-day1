import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def main() -> None:
    """
    Day 1: Context Failure → Context Fix

    This script intentionally shows:
    1) How naïve, stateless LLM calls can lose context.
    2) How message-based invocation preserves conversation history.
    """

    # Load environment variables from .env (API keys, etc.)
    load_dotenv()

    # You can switch to ChatGoogleGenerativeAI if you prefer, as long as you
    # keep the same overall behavior.
    llm = ChatOpenAI(temperature=0.0)

    # ---------------------------------------------------------------------
    # 1) Context break demonstration (naïve string-based invocation)
    # ---------------------------------------------------------------------
    print("=== Naive, stateless calls (context can break) ===")

    # Example from the assignment brief.
    resp1 = llm.invoke(
        "We are building an AI system for processing medical insurance claims."
    )
    print("resp1:", resp1)

    resp2 = llm.invoke("What are the main risks in this system?")
    print("resp2:", resp2)

    # Another classic context-break example: follow-up that relies on pronouns.
    pm_resp1 = llm.invoke("Who is the current PM of India?")
    print("pm_resp1:", pm_resp1)

    pm_resp2 = llm.invoke("What is his age?")
    print("pm_resp2:", pm_resp2)

    # In both of these cases, the model is not guaranteed to remember the
    # earlier question, because each call is stateless. The second question
    # may fail or behave inconsistently without conversation history.

    # ---------------------------------------------------------------------
    # 2) Context fix using Messages API
    # ---------------------------------------------------------------------
    print("\n=== Message-based invocation (context preserved) ===")

    messages = [
        SystemMessage(
            content=(
                "You are a senior AI architect reviewing production AI systems. "
                "Be precise and highlight real-world failure modes."
            )
        ),
        HumanMessage(
            content=(
                "We are building an AI system for processing medical insurance claims."
            )
        ),
        HumanMessage(content="What are the main risks in this system?"),
    ]

    result = llm.invoke(messages)
    print("messages_result:", result)


if __name__ == "__main__":
    main()

"""
Reflection:

1. Why did string-based invocation fail?
   - Each call like llm.invoke("...") is stateless; the model is not guaranteed
     to remember earlier inputs, so follow‑up questions (e.g. asking for risks
     or "his age" after "PM of India") may be answered without proper context.

2. Why does message-based invocation work?
   - By passing a messages list with SystemMessage and HumanMessage entries,
     we give the model the full conversation history in one call, so it can
     reason over prior turns and maintain consistent state.

3. What would break in a production AI system if we ignore message history?
   - User experiences become inconsistent, follow‑ups can be wrong or unsafe,
     and any downstream automation (approvals, data writes, decisions) built on
     top of those responses can fail in subtle, high‑impact ways.
"""

