from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
import operator

from langgraph.graph import StateGraph, END


class SupportState(TypedDict):
    """
    Shared state for the support routing graph.

    This mirrors the Day 2 assignment requirements:
    - messages: conversation history
    - should_escalate: whether the issue should be escalated
    - issue_type: free-form string you can use later
    - user_tier: "vip" or "standard"
    """

    messages: Annotated[list[BaseMessage], operator.add]
    should_escalate: bool
    issue_type: str
    user_tier: str


def check_user_tier_node(state: SupportState) -> dict:
    """
    Decide if user is VIP or standard (mock implementation).

    In a real system you'd look up the user in a database.
    Here we just inspect the first message content.
    """

    first_message = state["messages"][0].content.lower() if state["messages"] else ""
    if "vip" in first_message or "premium" in first_message:
        tier = "vip"
    else:
        tier = "standard"

    print(f"[check_user_tier_node] user_tier = {tier}")
    return {"user_tier": tier}


def vip_agent_node(state: SupportState) -> dict:
    """
    VIP path – fast lane / no escalation.

    For now we just set should_escalate = False and leave room
    to plug in an LLM-based response in later weeks.
    """

    print("[vip_agent_node] Handling VIP user with fast-lane policy")
    return {
        "should_escalate": False,
    }


def standard_agent_node(state: SupportState) -> dict:
    """
    Standard path – may escalate.

    For this assignment we simply set should_escalate = True
    to simulate that standard users may require escalation.
    """

    print("[standard_agent_node] Handling standard user, marking for escalation")
    return {
        "should_escalate": True,
    }


def route_by_tier(state: SupportState) -> str:
    """
    Route based on user tier.

    This function is wired into add_conditional_edges and must return
    either "vip_path" or "standard_path".
    """

    tier = state.get("user_tier", "").lower()
    if tier == "vip":
        print("[route_by_tier] Routing to VIP path")
        return "vip_path"
    print("[route_by_tier] Routing to standard path")
    return "standard_path"


def build_graph():
    workflow = StateGraph(SupportState)

    workflow.add_node("check_tier", check_user_tier_node)
    workflow.add_node("vip_agent", vip_agent_node)
    workflow.add_node("standard_agent", standard_agent_node)

    workflow.set_entry_point("check_tier")

    workflow.add_conditional_edges(
        "check_tier",
        route_by_tier,
        {
            "vip_path": "vip_agent",
            "standard_path": "standard_agent",
        },
    )

    workflow.add_edge("vip_agent", END)
    workflow.add_edge("standard_agent", END)

    return workflow.compile()


def main() -> None:
    # Load env in case you want to plug in LLMs later
    load_dotenv()

    graph = build_graph()

    print("=" * 60)
    print("VIP test run")
    print("=" * 60)
    vip_result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="I'm a VIP customer, please check my order status")
            ],
            "should_escalate": False,
            "issue_type": "",
            "user_tier": "",
        }
    )
    print(
        "VIP result:",
        "user_tier=",
        vip_result.get("user_tier"),
        "should_escalate=",
        vip_result.get("should_escalate"),
    )

    print("\n" + "=" * 60)
    print("Standard test run")
    print("=" * 60)
    standard_result = graph.invoke(
        {
            "messages": [HumanMessage(content="Check my order status")],
            "should_escalate": False,
            "issue_type": "",
            "user_tier": "",
        }
    )
    print(
        "Standard result:",
        "user_tier=",
        standard_result.get("user_tier"),
        "should_escalate=",
        standard_result.get("should_escalate"),
    )


if __name__ == "__main__":
    main()

