from dataclasses import dataclass
from typing import List, Dict

from .dictionary_builder import read_in_words, Words_
from .guess_validator import validate_results
from .game_print import print_game_start, print_help
from .utils import check_word_score


@dataclass
class GameWord:

    all_words: List[Words_]

    def __post_init__(self) -> None:
        self.current_words: List[Words_] = self.all_words

    def update_guess(self, word: str, result: str) -> None:
        word = word.upper()
        no_matches = self.filter_no_matches(word, result)
        partial_matches = self.filter_matched_with_wrong_position(word, result)
        complete_matches = self.filter_matched_with_right_position(word, result)
        positive_matches = list(partial_matches.values()) + list(
            complete_matches.values()
        )
        no_matches = self.remove_positive_matches(no_matches, positive_matches)

        self.filter_current_words_by_content(no_matches, positive_matches)
        self.filter_current_words_by_position(partial_matches, complete_matches)

    def remove_positive_matches(self, no_matches: list, positive_matches: list) -> None:
        for match in positive_matches:
            try:
                no_matches.remove(match)
            except ValueError:
                pass
        return no_matches

    def filter_current_words_by_content(
        self, negative_matches: List[str], positive_matches: List[str]
    ) -> None:
        self.current_words = [
            x
            for x in self.current_words
            if all(y not in x.word for y in negative_matches)
        ]
        self.current_words = [
            x for x in self.current_words if all(y in x.word for y in positive_matches)
        ]

    def filter_current_words_by_position(
        self, partial_matches: Dict[int, str], complete_matches: Dict[int, str]
    ) -> None:
        for k, v in complete_matches.items():
            self.current_words = [x for x in self.current_words if x.word[k] == v]
        for k, v in partial_matches.items():
            self.current_words = [x for x in self.current_words if x.word[k] != v]

    @staticmethod
    def filter_no_matches(word: str, result: str) -> List[str]:
        return [word[idx] for idx, x in enumerate(result) if x == "-"]

    @staticmethod
    def filter_matched_with_wrong_position(word: str, result: str) -> Dict[int, str]:
        return {idx: word[idx] for idx, x in enumerate(result) if x == "*"}

    @staticmethod
    def filter_matched_with_right_position(word: str, result: str) -> Dict[int, str]:
        return {idx: word[idx] for idx, x in enumerate(result) if x == "+"}


def main() -> None:

    print_game_start()
    game_word = GameWord(read_in_words())
    previous_word = "OATEN"
    while True:
        result = input(f"Enter results for word {previous_word}: ")
        if result == "help":
            print_help()
            continue
        elif result == "quit":
            print("See you later!")
            return
        elif not validate_results(result):
            continue
        else:
            game_word.update_guess(previous_word, result)
            remaining_words = game_word.current_words
            previous_word = remaining_words[0].word
            print(f"Possible words remaining is {len(remaining_words)}.")
            if len(remaining_words) == 1:
                print(f"Congratulations!! Word found: {previous_word}")
                return
        continue


if __name__ == "__main__":
    main()
