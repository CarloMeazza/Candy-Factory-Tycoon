def format_large_number(value: float) -> str:
    """
    Format a given number with a suitable large number suffix (K, M, B, T, etc.)
    """
    # List of suffixes that can be used to format the number
    # The list is a combination of the first letter of the alphabet with the
    # first letter of the alphabet, but with the first letter of the alphabet
    # in uppercase and the second letter in lowercase (e.g. "aA", "bB", etc.)
    suffixes: list[str] = ["", "K", "M", "B", "T"] + [
        f"{chr(65 + i // 26)}{chr(65 + i % 26)}" for i in range(0, 26 * 26)
    ]
    # The index of the suffix to use
    index: int = 0
    # Loop through the suffixes list until the value is < 1000 or the end of the list is reached
    while value >= 1000 and index < len(suffixes) - 1:
        # Divide the value by 1000 and increment the index
        value /= 1000.0
        index += 1
    # Return the formatted string with the value and the appropriate suffix
    return f"{value:.2f}{suffixes[index]}"
