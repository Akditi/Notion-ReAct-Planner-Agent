from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from agent.bot import create_react_agent_custom
from utils.logger import get_logger
from tools.notion_calender import get_calendar_events, add_calendar_event
from tools.notion_notes import get_notes, add_note
from tools.weather import get_weather 




