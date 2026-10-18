# Architecture

```text
User Task
   │
   ▼
Planner
   │
   ▼
State Machine
 PLAN → ACT → OBSERVE
          │
          ├─ success → next tool
          │
          └─ failure → RETRY → ACT
   │
   ▼
Tool Registry
 ├─ search_literature
 ├─ extract_evidence
 └─ synthesize_answer
   │
   ▼
Structured Step Log
   │
   ▼
Final Grounded Result
```

The project intentionally uses deterministic mock tools so orchestration,
state management, retries, observability, and testing can be demonstrated
without depending on external APIs.
