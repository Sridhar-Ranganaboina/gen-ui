def compose(candidate_id: str, context: dict) -> dict:
    if candidate_id == "manager-pending-approvals-card":
        return {"title": "You have pending approvals", "body": "3 approvals are waiting for your review."}
    return {"title": "Welcome back", "body": "No personalized content right now."}
