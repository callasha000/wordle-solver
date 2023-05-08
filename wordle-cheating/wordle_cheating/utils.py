from typing import List

from .dictionary_builder import Words_

def filter_duplicate_letter_words(words: List[Words_]) -> List[Words_]:
    return [word for word in words if word.no_duplicates]

def check_word_score(word: str) -> float:
    word_obj = Words_(word)
    return word_obj.word_score