from dataclasses import dataclass
from pathlib import Path
from typing import List

from .constants import LETTER_SCORE


@dataclass
class Words_:

    word: str
    word_score: float = 0.0

    def __post_init__(self) -> None:
        self.word = self.word.upper()
        self.update_word_score()

    def update_word_score(self) -> None:
        """Calculates word score based on summation of letter scores"""
        self.word_score = sum(LETTER_SCORE[letter.upper()] for letter in self.word)


def read_in_words() -> List[Words_]:
    """Read in all 5 letter words into a list of words"""
    script_path_parts = Path(__file__).parts[:-1]
    words_file_path = Path(*script_path_parts).joinpath("words.txt")
    words_list: List[Words_] = []
    with open(words_file_path) as file:
        words_list.extend(
            Words_(line.strip()) for line in file if len(line.strip()) == 5
        )
    return words_list
