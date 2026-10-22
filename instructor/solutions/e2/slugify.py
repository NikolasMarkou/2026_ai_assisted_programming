import re
import unicodedata


def slugify(text: str) -> str:
    """Return a URL slug for text: lowercase ASCII words joined by single hyphens."""
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", ascii_text.lower().replace("'", ""))
    return "-".join(words)
