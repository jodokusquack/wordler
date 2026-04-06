import pytest

from tests.shared_test_cases import test_cases
from wordler.utilities.text_handling import parse_wordle_share_text


# The test cases
@pytest.mark.parametrize(
    "input_text, expected_dict",
    [
        (
            test_cases["tc_success_1"],
            {
                "wordle_id": 1715,
                "guesses_needed": 4,
                "solved": True,
                "hard_mode": True,
                "guesses": """⬛️⬛️⬛️⬛️🟩
⬛⬛️⬛️⬛️🟩
⬛️🟨⬛️⬛️🟩
🟩🟩🟩🟩🟩""".split(
                    "\n"
                ),
            },
        ),
        (
            test_cases["tc_success_2"],
            {
                "wordle_id": 1715,
                "guesses_needed": 4,
                "solved": True,
                "hard_mode": False,
                "guesses": """⬛️⬛️🟨⬛️⬛️
🟨⬛️⬛️⬛️🟨
🟩⬛️🟩🟩⬛️
🟩🟩🟩🟩🟩""".split(
                    "\n"
                ),
            },
        ),
        (
            test_cases["tc_success_3"],
            {
                "wordle_id": 1713,
                "guesses_needed": 5,
                "solved": True,
                "hard_mode": False,
                "guesses": """⬜️⬜️⬜️⬜️🟨
⬜️🟨🟨🟨⬜️
⬜️🟩🟩🟨⬜️
⬜️🟩🟩🟩🟩
🟩🟩🟩🟩🟩""".split(
                    "\n"
                ),
            },
        ),
        (
            test_cases["tc_success_4"],
            {
                "wordle_id": 1713,
                "guesses_needed": 2,
                "solved": True,
                "hard_mode": True,
                "guesses": """⬛️🟨⬛️⬛️🟨
🟩🟩🟩🟩🟩""".split(
                    "\n"
                ),
            },
        ),
        (
            test_cases["tc_first_try"],
            {
                "wordle_id": 1702,
                "guesses_needed": 1,
                "solved": True,
                "hard_mode": False,
                "guesses": """🟩🟩🟩🟩🟩""".split("\n"),
            },
        ),
        (
            test_cases["tc_extra_text"],
            {
                "wordle_id": 1701,
                "guesses_needed": 4,
                "solved": True,
                "hard_mode": False,
                "guesses": """⬜️🟨⬜️⬜️🟨
⬜️⬜️🟨🟩⬜️
🟨⬜️🟨🟩⬜️
🟩🟩🟩🟩🟩""".split(
                    "\n"
                ),
            },
        ),
        (test_cases["tc_wrong_text"], None),
        (
            test_cases["tc_fail_1"],
            {
                "wordle_id": 1715,
                "guesses_needed": 7,
                "solved": False,
                "hard_mode": False,
                "guesses": """⬛⬛⬛⬛🟨
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛
🟩⬛⬛⬛⬛
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛""".split(
                    "\n"
                ),
            },
        ),
    ],
)
def test_parse_wordle_share_text(input_text, expected_dict):
    assert parse_wordle_share_text(input_text) == expected_dict
