import hashlib

def assign_variant(employee_id: str, app_id: str, surface: str) -> str:
    seed = f"{employee_id}:{app_id}:{surface}".encode()
    bucket = int(hashlib.sha256(seed).hexdigest()[:8], 16) % 100
    return "A" if bucket < 50 else "B"
