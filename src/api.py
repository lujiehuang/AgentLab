from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.agent import ResearchAgent

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "data" / "agent_steps.jsonl"

app = FastAPI(title="AgentLab API", version="0.1.0")

class RunRequest(BaseModel):
    task: str = Field(min_length=3)
    induce_transient_failure: bool = False

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run_agent(req: RunRequest):
    agent = ResearchAgent(max_retries=2, log_path=LOG)
    return agent.run(
        req.task,
        induce_transient_failure=req.induce_transient_failure
    ).model_dump()
