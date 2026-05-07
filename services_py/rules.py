def evaluate_rules(context: dict, memory: dict) -> dict:
    role_ctx = (context or {}).get("roleContext", {})
    mem_role = (memory or {}).get("roleContext", {})
    is_manager = bool(role_ctx.get("isManager") or mem_role.get("isManager"))
    if is_manager:
        return {"candidateId": "manager-pending-approvals-card", "reasonCodes": ["RULE_MANAGER"]}
    return {"candidateId": "default-dashboard-card", "reasonCodes": ["FALLBACK_DEFAULT"]}
