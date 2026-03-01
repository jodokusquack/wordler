import pytest
from src.text_handling import parse_wordle_share_text

test_case_1 = """Wordle 1,715 4/6*

⬛️⬛️⬛️⬛️🟩
⬛️⬛️⬛️⬛️🟩
⬛️🟨⬛️⬛️🟩
🟩🟩🟩🟩🟩"""

test_case_2 = """Wordle 1715 4/6

⬛️⬛️🟨⬛️⬛️
🟨⬛️⬛️⬛️🟨
🟩🟩🟩🟩⬛️
🟩🟩🟩🟩🟩"""

test_case_3 = """Wordle 1713 5/6

⬜️⬜️⬜️⬜️🟨
⬜️🟨🟨🟨⬜️
⬜️🟩🟩🟨⬜️
⬜️🟩🟩🟩🟩
🟩🟩🟩🟩🟩"""

test_case_4 = """Wordle 1,713 2/6*

⬛️🟨⬛️⬛️🟨
🟩🟩🟩🟩🟩"""

test_case_5 = """Wordle 1702 1/6

🟩🟩🟩🟩🟩"""

test_case_6 = """Look at my score:
Wordle 1,701 4/6

⬜️🟨⬜️⬜️🟨
⬜️⬜️🟨🟩⬜️
🟨⬜️🟨🟩⬜️
🟩🟩🟩🟩🟩

Its pretty good right? ♥️
"""

test_case_7 = """I solved it too:
it took me only 2/6 tries. I swear!"""

test_case_8 = """Wordle 1.715 X/6

⬛⬛⬛⬛🟨
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛
🟩⬛⬛⬛⬛
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛"""


# The test cases
@pytest.mark.parametrize("input_text, expected_dict", [
    (test_case_1,
     {'wordle_id': 1715,
      'guesses_needed': 4,
      'solved': True,
      'hard_mode': True,
      'guesses': """⬛️⬛️⬛️⬛️🟩
⬛️⬛️⬛️⬛️🟩
⬛️🟨⬛️⬛️🟩
🟩🟩🟩🟩🟩""".split('\n')
      }
     ),
    (test_case_2,
     {'wordle_id': 1715,
      'guesses_needed': 4,
      'solved': True,
      'hard_mode': False,
      'guesses': """⬛️⬛️🟨⬛️⬛️
🟨⬛️⬛️⬛️🟨
🟩🟩🟩🟩⬛️
🟩🟩🟩🟩🟩""".split('\n')
      }
     ),
    (test_case_3,
     {'wordle_id': 1713,
      'guesses_needed': 5,
      'solved': True,
      'hard_mode': False,
      'guesses': """⬜️⬜️⬜️⬜️🟨
⬜️🟨🟨🟨⬜️
⬜️🟩🟩🟨⬜️
⬜️🟩🟩🟩🟩
🟩🟩🟩🟩🟩""".split('\n')
      }
     ),
    (test_case_4,
     {'wordle_id': 1713,
      'guesses_needed': 2,
      'solved': True,
      'hard_mode': True,
      'guesses': """⬛️🟨⬛️⬛️🟨
🟩🟩🟩🟩🟩""".split('\n')
      }
     ),
    (test_case_5,
     {'wordle_id': 1702,
      'guesses_needed': 1,
      'solved': True,
      'hard_mode': False,
      'guesses': """🟩🟩🟩🟩🟩""".split('\n')
      }
     ),
    (test_case_6,
     {'wordle_id': 1701,
      'guesses_needed': 4,
      'solved': True,
      'hard_mode': False,
      'guesses': """⬜️🟨⬜️⬜️🟨
⬜️⬜️🟨🟩⬜️
🟨⬜️🟨🟩⬜️
🟩🟩🟩🟩🟩""".split('\n')
      }
     ),
    (test_case_7,
     None
     ),
    (test_case_8,
     {'wordle_id': 1715,
      'guesses_needed': 7,
      'solved': False,
      'hard_mode': False,
      'guesses': """⬛⬛⬛⬛🟨
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛
🟩⬛⬛⬛⬛
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛""".split('\n')
      }
     ),
    ])
def test_parse_wordle_share_text(input_text, expected_dict):
    assert parse_wordle_share_text(input_text) == expected_dict
