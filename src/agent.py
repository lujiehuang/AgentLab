from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from src.models import AgentResult, StepRecord, ToolCall
from src.tools import TOOLS, ToolError

class ResearchAgent:
    """Deterministic agent workflow with state, tool calls, retries, and logs."""

    def __init__(self, max_retries: int = 2, log_path: str | Path | None = None):
        self.max_retries = max_retries
        self.log_path = Path(log_path) if log_path else None
        self.steps: list[StepRecord] = []
        self.tool_calls = 0
        self.retries = 0
        self._step_id = 0

    def _record(self, state: str, message: str, **kwargs):
        self._step_id += 1
        rec = StepRecord(step_id=self._step_id, state=state, message=message, **kwargs)
        self.steps.append(rec)
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(rec.model_dump_json() + "\n")

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.tool_calls += 1
        call = ToolCall(name=name, arguments=arguments)
        for attempt in range(1, self.max_retries + 2):
            self._record("ACT", f"Calling tool: {name}", tool_call=call, attempt=attempt)
            try:
                out = TOOLS[name].run(**arguments)
                self._record("OBSERVE", f"Tool succeeded: {name}", observation=out, attempt=attempt)
                return out
            except ToolError as e:
                if attempt <= self.max_retries:
                    self.retries += 1
                    self._record("RETRY", f"{name} failed: {e}", attempt=attempt)
                else:
                    self._record("FAILED", f"{name} exhausted retries: {e}", attempt=attempt)
                    raise

    def run(self, task: str, induce_transient_failure: bool = False) -> AgentResult:
        self.steps = []
        self.tool_calls = 0
        self.retries = 0
        self._step_id = 0

        self._record(
            "PLAN",
            "Plan: search literature -> extract evidence -> synthesize grounded answer."
        )

        try:
            found = self._call_tool(
                "search_literature",
                {"query": task, "fail_once": induce_transient_failure},
            )
            evidence = self._call_tool(
                "extract_evidence",
                {"results": found["results"]},
            )
            synthesis = self._call_tool(
                "synthesize_answer",
                {"task": task, "evidence": evidence["evidence"]},
            )
            self._record("DONE", "Workflow completed successfully.")
            return AgentResult(
                task=task,
                status="completed",
                answer=synthesis["answer"],
                steps=self.steps,
                tool_calls=self.tool_calls,
                retries=self.retries,
            )
        except Exception as e:
            return AgentResult(
                task=task,
                status="failed",
                answer=f"Workflow failed: {e}",
                steps=self.steps,
                tool_calls=self.tool_calls,
                retries=self.retries,
            )
