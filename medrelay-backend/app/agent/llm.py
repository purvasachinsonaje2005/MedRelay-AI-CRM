"""Groq LLM client wrapped via langchain-groq."""
import os
from langchain_groq import ChatGroq


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to .env (see .env.example)."
        )
    model = os.getenv("GROQ_MODEL", "mllama-3.3-70b-versatile")
    return ChatGroq(model=model, api_key=api_key, temperature=0.2)
