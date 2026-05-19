"""LangGraph workflow that wires the LLM to the 5 tools.

Flow:
   ┌─────────┐  tool_calls?  ┌───────┐
   │  agent  │──────────────▶│ tools │
   └─────────┘◀──────────────└───────┘
        │ no tool_calls
        ▼
       END
"""
from typing import Annotated, TypedDict, List
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from .llm import get_llm
from .tools import TOOLS, bind_db


SYSTEM_PROMPT = """You are MedRelay, an assistant for pharmaceutical field
reps logging interactions with Healthcare Professionals (HCPs).

When the user describes a visit, you must:
  1. Extract the doctor name, hospital name, specialty, interaction type,
     notes, and follow-up date.
  2. Call SummarizeInteractionTool to produce a concise summary.
  3. Call FollowUpRecommendationTool to produce concrete next steps.
  4. Call LogInteractionTool to persist the interaction.
  5. Reply to the rep with a short confirmation plus the suggested follow-ups.

When the user asks about past interactions, call InteractionHistoryTool.
When the user asks to fix or update a record, call EditInteractionTool.

Always be concise and professional. Dates must always use current/future year in ISO format (YYYY-MM-DD)..
"""


class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]


def _build_graph():
    llm = get_llm().bind_tools(TOOLS)
    tool_node = ToolNode(TOOLS)

    def agent_node(state: AgentState):
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: AgentState):
        last = state["messages"][-1]
        if getattr(last, "tool_calls", None):
            return "tools"
        return END

    g = StateGraph(AgentState)
    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    return g.compile()


_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = _build_graph()
    return _graph


def run_agent(message: str, db) -> dict:
    """Run the agent on a user message. Returns a dict suitable for AgentResponse."""
    bind_db(db)
    try:
        graph = get_graph()
        result = graph.invoke(
            {"messages": [SystemMessage(SYSTEM_PROMPT), HumanMessage(message)]}
        )
    finally:
        bind_db(None)

    messages = result["messages"]
    tool_calls: List[str] = []
    summary = ""
    recommendations: List[str] = []
    interaction_id = None
    draft: dict = {}

    for m in messages:
        for tc in getattr(m, "tool_calls", None) or []:
            name = tc.get("name") if isinstance(tc, dict) else tc.name
            args = tc.get("args") if isinstance(tc, dict) else tc.args
            tool_calls.append(name)
            if name == "LogInteractionTool" and args:
                draft = dict(args)
            elif name == "SummarizeInteractionTool" and args and "notes" in args:
                pass  # summary captured from tool message below

    # Tool messages carry the return values.
    from langchain_core.messages import ToolMessage
    for m in messages:
        if isinstance(m, ToolMessage):
            content = m.content if isinstance(m.content, str) else str(m.content)
            if m.name == "SummarizeInteractionTool":
                summary = content.strip().strip('"')
            elif m.name == "FollowUpRecommendationTool":
                try:
                    import json
                    recommendations = json.loads(content) if content.startswith("[") else [content]
                except Exception:
                    recommendations = [content]
            elif m.name == "LogInteractionTool":
                try:
                    import json
                    parsed = json.loads(content) if isinstance(content, str) else content
                    interaction_id = parsed.get("id")
                except Exception:
                    pass

    final = messages[-1]
    reply = final.content if isinstance(final.content, str) else str(final.content)

    return {
        "reply": reply,
        "draft": draft,
        "summary": summary,
        "recommendations": recommendations,
        "tool_calls": tool_calls,
        "interaction_id": interaction_id,
    }
