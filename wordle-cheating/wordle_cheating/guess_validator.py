from .constants import OPTIONS


def validate_results(guess: str) -> bool:
    options_ = OPTIONS

    if len(guess) != 5:
        print("Too many characters entered. try again...")
        return False

    wrong_characters = [character for character in guess if character not in options_]
    if wrong_characters:
        print(
            f"invalid character values: {', '.join(list(wrong_characters))}, please reenter results..."
        )
        return False

    return True
