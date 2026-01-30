def needs_context(prompt: str) -> bool:
    reference_words = ["it", "this", "that", "previous", "above", "earlier", "continue", "modify", "update"]
    verbs = ["add", "remove", "change", "fix", "improve", "extend"]

    lower = prompt.lower().strip()

    if any(word in lower for word in reference_words):
        return True

    if any(lower.strip().startswith(v) for v in verbs):
        return True

    return False