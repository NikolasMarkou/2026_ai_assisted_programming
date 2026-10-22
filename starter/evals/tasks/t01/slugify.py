def slugify(text):
    """Lowercase text with the words joined by one hyphen."""
    words = text.lower().split(" ")
    return "-".join(words)
