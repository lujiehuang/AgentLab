from src.agent import ResearchAgent

if __name__ == "__main__":
    agent = ResearchAgent(max_retries=2)
    result = agent.run(
        "How can reflective interventions reduce over-reliance on AI advice?",
        induce_transient_failure=True,
    )
    print(result.model_dump_json(indent=2))
