def page_count(total_items, per_page):
    """Number of pages needed to show total_items, per_page on each page."""
    if per_page < 1:
        raise ValueError("per_page must be 1 or more")
    return total_items // per_page
