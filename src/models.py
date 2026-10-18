from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)

class StepRecord(BaseModel):
    step_id: int
    state: Literal["PLAN", "ACT", "OBSERVE", "RETRY", "DONE", "FAILED"]
    message: str
    tool_call: ToolCall | None = None
    observation: dict[str, Any] | None = None
    attempt: int = 1

class AgentResult(BaseModel):
    task: str
    status: Literal["completed", "failed"]
    answer: str
    steps: list[StepRecord]
    tool_calls: int
    retries: int
