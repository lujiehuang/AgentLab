# AgentLab

**Tool-using research agent with state management, retry logic, observability, and API serving**

AgentLab is a compact agent-engineering project designed to demonstrate the infrastructure behind reliable LLM-agent workflows rather than just a chatbot interface.

## What it demonstrates

- task planning
- tool registry
- explicit workflow state
- tool calling
- observation handling
- retry / error recovery
- structured step logging
- deterministic offline testing
- FastAPI serving
- CI smoke testing

## Workflow

```text
Task
 │
 ▼
PLAN
 │
 ▼
ACT ───────► Tool
 │            │
 │            ▼
 │         Result/Error
 │            │
 ▼            │
OBSERVE ◄─────┘
 │
 ├─ error → RETRY → ACT
 │
 └─ success → next tool
 │
 ▼
DONE
```

The demo agent runs:

1. `search_literature`
2. `extract_evidence`
3. `synthesize_answer`

A transient tool failure can be intentionally injected to show recovery behavior.

## Quick start

```bash
pip install -r requirements.txt
python src/demo.py
uvicorn src.api:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Example request:

```json
{
  "task": "How can reflective interventions reduce over-reliance on AI advice?",
  "induce_transient_failure": true
}
```

## Why offline mock tools?

The goal of this repository is to make **agent orchestration** inspectable and reproducible. External LLM or search APIs can be added later, but the core engineering concepts can already be tested:

- state transitions
- tool dispatch
- retries
- logging
- failure handling
- deterministic evaluation

## Research roadmap

1. Add a real LLM planner.
2. Add structured function-calling schemas.
3. Add web/search connectors.
4. Add citation verification.
5. Add persistent memory.
6. Add cost / latency tracing.
7. Add agent-evaluation benchmarks.
8. Add human approval checkpoints.

## Author

Lujie Huang  
https://lujiehuang.github.io/
