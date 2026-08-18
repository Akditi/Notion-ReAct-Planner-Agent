import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools.notion_notes import get_notes, add_note
from tools.notion_calendar import get_calendar_events, add_calendar_event
from utils.logger import get_logger
from utils.groq_models import get_default_groq_model

logger = get_logger(__name__)


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("Groq api key not set")
        raise ValueError("Groq api key not set")

    # Set GROQ_MODEL to pin a specific model; otherwise auto-detect the best
    # currently-available free Groq model so this doesn't silently break
    # whenever Groq retires a hardcoded model ID.
    model = os.getenv("GROQ_MODEL") or get_default_groq_model(api_key)
    logger.info(f"Using Groq model: {model}")

    return ChatGroq(
        model=model,
        temperature=0.5,
        api_key=api_key
    )

def create_react_agent_custom():
    logger.info("Initializing Agent")
    llm = get_llm()

    tools = [get_notes, add_note, get_calendar_events, add_calendar_event]

    try:
        agent = create_agent(model=llm, tools=tools)
        logger.info("Agent Initialized")
        return agent

    except TypeError as e:
        logger.error(f"Failed to create agent: {e}")
        raise e