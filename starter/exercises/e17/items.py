"""Three small helpers for an order list. Each has one bug; fix_plan.md names them."""


def clean_name(text):
    """Trim the ends and keep one space between words: ' red  pen ' gives 'red pen'."""
    return text.replace(" ", "")


def to_cents(text):
    """Turn a price text into whole cents: '19.99' gives 1999."""
    return int(float(text) * 100)


def largest(values, n):
    """The n biggest values, biggest first."""
    return sorted(values)[:n]
