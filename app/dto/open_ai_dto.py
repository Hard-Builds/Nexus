from typing import Optional

from pydantic import BaseModel


class OpenAIChatReqDto(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[int] = None
    top_p: Optional[int] = None
    frequency_penalty: Optional[int] = None
    presence_penalty: Optional[int] = None
    logit_bias: Optional[int] = None
    n: Optional[int] = None
    seed: Optional[int] = None
    stop: Optional[int] = None
    stream: Optional[int] = None
    user: Optional[int] = None
