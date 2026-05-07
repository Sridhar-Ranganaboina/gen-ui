import time
from services_py.experimentation import assign_variant
from services_py.llm_composer import compose
from services_py.memory import get_memory
from services_py.policy import validate_content
from services_py.registry import validate_slot
from services_py.rules import evaluate_rules


def evaluate_decision(request: dict) -> dict:
    app_id = request["appId"]
    slot = request["slot"]
    surface = request.get("surface", "employee-dashboard")
    if not validate_slot(app_id, surface, slot):
        return {
            "decisionId": f"dec_{int(time.time() * 1000)}",
            "candidateId": "invalid-slot-fallback",
            "reasonCodes": ["REGISTRY_SLOT_INVALID", "FALLBACK_DEFAULT"],
            "manifest": {"schemaVersion": "1.0.0", "surface": surface, "slot": slot, "components": []},
            "audit": {"policyStatus": "not_applicable", "ruleHits": ["REGISTRY_SLOT_INVALID"]},
        }

    memory = get_memory(request["employeeId"])
    dismissed = set(memory.get("behavioralMemory", {}).get("recentDismissedCards", []))
    choice = evaluate_rules(request.get("context", {}), memory)
    fallback = choice["candidateId"] == "manager-pending-approvals-card" and choice["candidateId"] in dismissed
    candidate = "default-dashboard-card" if fallback else choice["candidateId"]
    reasons = ["SUPPRESSED_DISMISSED", "FALLBACK_DEFAULT"] if fallback else choice["reasonCodes"]

    copy = compose(candidate, request.get("context", {}))
    is_valid, policy_error = validate_content(f"{copy['title']} {copy['body']}")
    if not is_valid:
        candidate = "policy-fallback-card"
        reasons = reasons + ["POLICY_BLOCK"]
        copy = {"title": "Welcome back", "body": "Content unavailable due to policy checks."}

    variant = assign_variant(request["employeeId"], app_id, surface)

    return {
        "decisionId": f"dec_{int(time.time() * 1000)}",
        "candidateId": candidate,
        "reasonCodes": reasons,
        "experiment": {"id": "exp-dashboard-hero", "variant": variant},
        "manifest": {
            "schemaVersion": "1.0.0",
            "surface": surface,
            "slot": slot,
            "components": [{
                "type": "summary_card",
                "id": candidate,
                "props": {
                    "title": copy["title"],
                    "body": copy["body"],
                    "cta": {"label": "Open", "action": "open_link", "target": "/approvals"},
                },
            }],
        },
        "audit": {"ruleHits": reasons, "modelVersion": "mock-llm-v1", "policyStatus": "pass" if is_valid else policy_error},
    }
