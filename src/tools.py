from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

class ToolError(RuntimeError):
    pass

@dataclass
class Tool:
    name: str
    description: str
    fn: Callable[..., dict[str, Any]]

    def run(self, **kwargs) -> dict[str, Any]:
        return self.fn(**kwargs)

def search_literature(query: str, fail_once: bool = False, _state={"failed": False}):
    """Offline mock literature search for workflow demonstration."""
    if fail_once and not _state["failed"]:
        _state["failed"] = True
        raise ToolError("temporary search backend timeout")

    corpus = [
        {
            "title": "Calibrating Reliance on AI Advice",
            "year": 2024,
            "venue": "CHI",
            "keywords": ["reliance", "verification", "human-ai"]
        },
        {
            "title": "Reflection Prompts in Human-AI Decision Making",
            "year": 2025,
            "venue": "CSCW",
            "keywords": ["reflection", "intervention", "human-ai"]
        },
        {
            "title": "Tool-Using Language Models for Research Workflows",
            "year": 2025,
            "venue": "ACL",
            "keywords": ["agents", "tools", "workflow"]
        },
    ]
    terms = set(query.lower().split())
    scored = []
    for item in corpus:
        hay = " ".join([item["title"], item["venue"], " ".join(item["keywords"])]).lower()
        score = sum(t in hay for t in terms)
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return {"results": [x[1] for x in scored[:3]]}

def extract_evidence(results: list[dict]) -> dict:
    return {
        "evidence": [
            f'{r["title"]} ({r["year"]}, {r["venue"]})'
            for r in results
        ]
    }

def synthesize_answer(task: str, evidence: list[str]) -> dict:
    if not evidence:
        raise ToolError("no evidence available")
    answer = (
        f"Task: {task}\n\n"
        "Evidence considered:\n- " + "\n- ".join(evidence) +
        "\n\nSynthesis: The retrieved evidence suggests that "
        "human-AI reliance, reflective interventions, and tool-using agents can be "
        "studied together through instrumented workflows with explicit verification steps."
    )
    return {"answer": answer}

TOOLS = {
    "search_literature": Tool(
        "search_literature",
        "Search a small offline scholarly corpus.",
        search_literature,
    ),
    "extract_evidence": Tool(
        "extract_evidence",
        "Convert retrieved records into compact evidence strings.",
        extract_evidence,
    ),
    "synthesize_answer": Tool(
        "synthesize_answer",
        "Produce a grounded synthesis from task + evidence.",
        synthesize_answer,
    ),
}
