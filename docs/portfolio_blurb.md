## AgentLab — Tool-Using Research Agent with Retry & State Management

**Python · LLM Agent Architecture · Tool Calling · State Machine · Retry Logic · FastAPI**

Built a deterministic research-agent prototype that decomposes a task into a multi-step workflow, calls tools through a registry, records explicit PLAN/ACT/OBSERVE/RETRY/DONE states, recovers from transient failures, and exposes the workflow through a FastAPI service. The offline tool layer makes the orchestration logic fully reproducible and testable.
