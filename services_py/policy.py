FORBIDDEN = {"guaranteed", "always", "never fail"}

def validate_content(text: str) -> tuple[bool, str | None]:
    lower = text.lower()
    for token in FORBIDDEN:
        if token in lower:
            return False, f"FORBIDDEN_CLAIM:{token}"
    return True, None
