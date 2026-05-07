REGISTRY = {
    "apps": {"employee-portal": {"channels": ["web"]}},
    "slots": {("employee-portal", "employee-dashboard", "dashboard-hero")},
    "actions": {"open_link", "dismiss", "open_modal", "create_task"},
}

def validate_slot(app_id: str, surface: str, slot: str) -> bool:
    return (app_id, surface, slot) in REGISTRY["slots"]
