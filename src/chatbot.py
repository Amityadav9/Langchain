# src/chatbot.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Load environment variables
load_dotenv()

# Get API keys
groq_api_key = os.getenv("GROQ_API_KEY")

use_langsmith = os.getenv("USE_LANGSMITH", "false").lower() == "true"

if use_langsmith:
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "CourseLanggraph"
# langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

# Set up LangSmith environment variables
# os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "CourseLanggraph"

# Initialize ChatGroq
llm = ChatGroq(groq_api_key=groq_api_key, model="Gemma2-9b-It")


# Define State class
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Build graph
graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": llm.invoke(state["messages"])}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def get_chatbot_response(user_input):
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            return value["messages"].content
