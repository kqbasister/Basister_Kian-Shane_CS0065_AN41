"""Count happy/sad words using the public Hu and Liu Opinion Lexicon."""

import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_words(filename):
    lines = (DATA_DIR / filename).read_text(encoding="utf-8").splitlines()
    return {line.strip().lower() for line in lines
            if line.strip() and not line.lstrip().startswith(";")}


HAPPY_WORDS = load_words("positive-words.txt")
SAD_WORDS = load_words("negative-words.txt")


def words(sentence):
    # Ignore case and punctuation; retain hyphens, apostrophes and a+.
    return re.findall(r"[^\W_]+(?:[-'][^\W_]+)*(?:\+)?",
                      sentence.lower().replace("\u2019", "'"))


def number_happy(sentence):
    return sum(word in HAPPY_WORDS for word in words(sentence))


def number_sad(sentence):
    return sum(word in SAD_WORDS for word in words(sentence))


def main():
    sentence = input("Enter a sentence: ")
    happy = number_happy(sentence)
    sad = number_sad(sentence)

    print(f"Happy words: {happy}")
    print(f"Sad words: {sad}")
    if happy > sad:
        print("Analysis: Positive (happy)")
    elif sad > happy:
        print("Analysis: Negative (sad)")
    else:
        print("Analysis: Neutral")


if __name__ == "__main__":
    main()
