
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
import time
from dataclasses import dataclass
from operator import add
from langchain_core.messages import ToolMessage, SystemMessage
from random import randint

from langchain_core.runnables import RunnableConfig
from langgraph.cache.memory import InMemoryCache
from langgraph.errors import GraphRecursionError
from langgraph.graph import MessagesState

from multiprocessing import resource_tracker, context

from langgraph.graph import StateGraph, START, END, MessagesState, MessageGraph
from typing import TypedDict, Literal, Sequence, Annotated, Final, Tuple
from IPython.display import display
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain.tools import tool
from langgraph.managed.is_last_step import RemainingSteps
from langsmith import traceable
from loguru import logger
from langgraph.types import Send, Command, CachePolicy, interrupt
from langchain.messages import HumanMessage, AIMessage, SystemMessage
load_dotenv(override=True)


model = ChatDeepSeek(
    model="deepseek-v4-flash",
    # temperature=0.7,
    extra_body={
        "thinking": {
            "type": "disabled",
        }
    }
)

class OverAllState(TypedDict):
    username: str # #%
    age: int # #
    gender: Literal["male", "female"] # #/

@traceable(name="get_info_node", run_type="chain")
def get_info_node(state: OverAllState) -> OverAllState:
    username=interrupt("请输入您的用户名:")
    age= interrupt("请输入您的年龄:")
    gender=interrupt("请输入您的性别:(male/female)")

    return {
        "username": username,
        "age": age,
        "gender": gender
    }

builder = StateGraph(state_schema=OverAllState)
builder.add_node("get_info_node", get_info_node)
builder.add_edge(START, "get_info_node")
builder.add_edge( "get_info_node", END)

graph = builder.compile()

display(graph)