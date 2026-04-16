"""LLM and observability platform clients."""
import os
from langsmith.wrappers import wrap_openai
from langsmith import Client as LangSmithClient
from openai import OpenAI
from langfuse import Langfuse
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# Ollama runs an OpenAI-compatible server locally by default
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

def get_openai_client():
    """
    Returns an Ollama client (OpenAI-compatible) with LangSmith tracing.
    Model is configurable via LLM_MODEL (default: qwen2.5-coder:7b).
    Requires Ollama running locally: https://ollama.com
    """
    return wrap_openai(
        OpenAI(
            base_url=OLLAMA_BASE_URL,
            api_key="ollama",
        )
    )

def get_judge_llm():
    """
    Returns a ChatOllama instance for use as a LangChain evaluator judge.
    Model is configurable via JUDGE_MODEL (default: qwen2.5-coder:1.5b).
    Temperature is fixed at 0 for consistent, deterministic judgments.
    """
    return ChatOllama(
        model=os.getenv("JUDGE_MODEL", "qwen2.5-coder:7b"),
        temperature=0,
    )

def get_model_name() -> str:
    return os.getenv("LLM_MODEL", "qwen2.5-coder:7b")

def get_temperature() -> float:
    return float(os.getenv("LLM_TEMPERATURE", "0"))

def get_langsmith_client():
    return LangSmithClient()

def get_langfuse_client():
    return Langfuse()

def get_openai_client_langfuse():
    """Returns Ollama client with Langfuse tracing."""
    from langfuse.openai import OpenAI as LangfuseOpenAI
    return LangfuseOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",
    )