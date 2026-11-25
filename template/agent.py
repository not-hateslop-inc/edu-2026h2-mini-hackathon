import uuid
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.types import interrupt, Command
from tracing import Trace

load_dotenv()
MAX_STEPS = 8


@tool
def read_something(query: str) -> str:
    """(읽기) 팀 주제에 맞게 바꾸세요."""
    return f"결과: {query}"


@tool
def write_something(content: str) -> str:
    """(쓰기) 실행 전에 사람 승인을 받는다."""
    if interrupt({"action": "write_something", "content": content}) != "yes":
        return "사용자가 취소함"
    return "완료"


TOOLS = [read_something, write_something]
llm = init_chat_model("openai:gpt-4o-mini", temperature=0).bind_tools(TOOLS)


def agent_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


g = StateGraph(MessagesState)
g.add_node("agent", agent_node)
g.add_node("tools", ToolNode(TOOLS, handle_tool_errors=True))
g.add_edge(START, "agent")
g.add_conditional_edges("agent", tools_condition)
g.add_edge("tools", "agent")
graph = g.compile(checkpointer=InMemorySaver())


def chat(q: str, thread: str) -> str:
    trace = Trace(thread)
    cfg = {"configurable": {"thread_id": thread}, "recursion_limit": 2 * MAX_STEPS}
    inp = {"messages": [("user", q)]}
    try:
        while True:
            for i, ev in enumerate(graph.stream(inp, cfg, stream_mode="updates")):
                trace.log(i, "update", nodes=list(ev))
            st = graph.get_state(cfg)
            if st.interrupts:
                ans = input(f"승인 요청 {st.interrupts[0].value} (yes/no) ")
                trace.log(-1, "approval", answer=ans)
                inp = Command(resume=ans)
                continue
            return st.values["messages"][-1].content
    except GraphRecursionError:
        trace.log(-1, "end", reason="max_steps")
        return "처리 단계가 너무 많아 멈췄습니다. 담당자에게 문의해 주세요."


if __name__ == "__main__":
    tid = uuid.uuid4().hex[:8]
    while (q := input("> ")) not in ("q", ""):
        print(chat(q, tid))
