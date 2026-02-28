# text_handling.py
import re


def parse_wordle_share_text(wordle_share_text: str) -> dict:
    """Use a regex to extract the results from the automatically generated Wordle Share message."""
    regex = re.compile(
        r"Wordle\s(?P<wordle_id>[\d+,]+)\s(?P<guesses_needed>[0-6X])/6(?P<hard_mode>\*?)\n{2}(?P<guesses>[🟨🟩⬛️⬜️\n]+[🟩🟩🟩🟩🟩])",
        flags=re.MULTILINE | re.UNICODE
    )
    m = regex.search(wordle_share_text)

    if not m:
        print("Couldn't extract Wordle stats.")
        return None
    else:
        result = dict()
        # extract the information from the match
        result['wordle_id'] = int(m['wordle_id'].replace(",", "").replace(".", ""))  # the wordle_no could contain , or . as thousands sep but is always an int

        if m['guesses_needed'] == 'X':
            result['guesses_needed'] = 7
        else:
            result['guesses_needed'] = int(m['guesses_needed'])

        result['solved'] = (result['guesses_needed'] <= 6)

        result['hard_mode'] = bool(m['hard_mode'])

        result['guesses'] = m['guesses'].split("\n")

        return result
