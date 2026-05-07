import unittest
from services_py.memory import seed_memory
from services_py.orchestrator import evaluate_decision

class TestOrchestrator(unittest.TestCase):
    def test_manager_gets_manager_card(self):
        seed_memory("E1", {"employeeId": "E1", "roleContext": {"isManager": True}, "behavioralMemory": {"recentDismissedCards": []}})
        decision = evaluate_decision({"appId": "employee-portal", "channel": "web", "surface": "employee-dashboard", "slot": "dashboard-hero", "employeeId": "E1"})
        self.assertEqual(decision["candidateId"], "manager-pending-approvals-card")
        self.assertIn("experiment", decision)

    def test_dismissed_is_suppressed(self):
        seed_memory("E2", {"employeeId": "E2", "roleContext": {"isManager": True}, "behavioralMemory": {"recentDismissedCards": ["manager-pending-approvals-card"]}})
        decision = evaluate_decision({"appId": "employee-portal", "channel": "web", "surface": "employee-dashboard", "slot": "dashboard-hero", "employeeId": "E2"})
        self.assertEqual(decision["candidateId"], "default-dashboard-card")

    def test_invalid_slot_fallback(self):
        decision = evaluate_decision({"appId": "employee-portal", "channel": "web", "surface": "employee-dashboard", "slot": "missing-slot", "employeeId": "E3"})
        self.assertEqual(decision["candidateId"], "invalid-slot-fallback")

if __name__ == '__main__':
    unittest.main()
