import os
import random

words_file_path = os.path.join(os.path.dirname(__file__), "words.txt")


def generate_memorable_password(n: int = 3) -> str:
    """Generate a memorable password consisting of n words."""
    with open(words_file_path, "r") as file:
        words = file.readlines()

    return "-".join(random.choice(words).strip() for _ in range(n))
