NUMERALS = ((1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"),
            (1, "I"))


def to_roman(number):
    """Roman numeral for 1 to 3999, with subtractive forms such as IV and IX."""
    if not 1 <= number <= 3999:
        raise ValueError("number must be from 1 to 3999")
    result = ""
    for value, letters in NUMERALS:
        while number >= value:
            result += letters
            number -= value
    return result
