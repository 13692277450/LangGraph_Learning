from langgraph.graph import StateGraph, START, END
# from dotenv import load_dotenv
from typing import TypedDict, Annotated
from operator import add
from IPython.display import Image, display


# load_dotenv()

class OverAllState(TypedDict):
    logs: Annotated[list[str],add]
    cur_id: str
    
def node_1(state: OverAllState) -> OverAllState:
    pre_id = state["cur_id"]
    return {
        "logs": ["node_1 running done"],
        "cur_id": pre_id + "_node_1"
    }
    

def node_2(state: OverAllState) -> OverAllState:
    pre_id = state["cur_id"]
    return {
        "logs": ["node_2 running done"],
        "cur_id": pre_id + "_node_2"
    }
    
builder = StateGraph(state_schema=OverAllState)
builder.add_node(node_1)
builder.add_node(node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)
graph = builder.compile()

result = graph.invoke({"logs": [], "cur_id": "start"})
png_bytes = graph.get_graph().draw_mermaid_png()
print(result)
png = Image(png_bytes)
display(png)
