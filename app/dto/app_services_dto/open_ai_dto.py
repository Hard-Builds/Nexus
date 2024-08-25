from typing import Dict, List, Optional

from pydantic import BaseModel


class OpenAIChatCompletion(BaseModel):
    portkey_api_key: str
    model: str
    messages: List[Dict]
    temperature: Optional[int]
