import unittest
from src.agent import ResearchAgent

class AgentLabTests(unittest.TestCase):
    def test_normal_run(self):
        result = ResearchAgent().run("human AI reliance")
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.tool_calls, 3)
        self.assertEqual(result.retries, 0)
        self.assertIn("Evidence considered", result.answer)

    def test_retry_recovery(self):
        result = ResearchAgent(max_retries=2).run(
            "reflection intervention",
            induce_transient_failure=True,
        )
        self.assertEqual(result.status, "completed")
        self.assertGreaterEqual(result.retries, 1)

    def test_state_trace_contains_done(self):
        result = ResearchAgent().run("agent workflows")
        states = [s.state for s in result.steps]
        self.assertIn("PLAN", states)
        self.assertIn("ACT", states)
        self.assertIn("OBSERVE", states)
        self.assertIn("DONE", states)

if __name__ == "__main__":
    unittest.main()
