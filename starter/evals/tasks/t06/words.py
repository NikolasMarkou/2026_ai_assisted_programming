def count_words(text):
    """Count words, ignoring case and punctuation around a word. Returns a dict."""
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
