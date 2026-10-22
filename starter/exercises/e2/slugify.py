def slugify(text: str) -> str:
    """Return a URL slug for text.

    Rules:
    - lowercase ASCII letters and digits only; accents are dropped to their base letter
    - every run of other characters becomes one hyphen
    - no hyphen at the start or the end
    - apostrophes are removed, not turned into hyphens
    - text with no letters or digits gives an empty string

    Examples:
        slugify("Hello, World!")  gives "hello-world"
        slugify("Café au lait")  gives "cafe-au-lait"
        slugify("  a -- b  ")     gives "a-b"
    """
    raise NotImplementedError("write slugify")
