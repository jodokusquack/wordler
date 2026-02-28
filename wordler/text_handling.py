# text_handling.py
import re


def parse_wordle_share_text(wordle_share_text: str) -> dict:
    """Use a regex to extract the results from the automatically generated Wordle Share message."""
    regex = re.compile(
        r"Wordle\s(?P<wordle_id>[\d+,.]+)\s(?P<guesses_needed>[0-6X])/6(?P<hard_mode>\*?)\n{2}(?P<guesses>(?:[🟨🟩⬛️⬜️]+\n?){1,6})",
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

        result['guesses'] = list(filter(lambda x: x != '', m['guesses'].split("\n")))  # filter to remove empty strings

        return result


def stats_reply_message(stats_dict: dict) -> str:
    if stats_dict['solved']:
        reply = f"""Congrats, you solved it in {stats_dict['guesses_needed']} tries. 🎈
Can you improve the next time? 👀"""
    else:
        if stats_dict['hard_mode']:
            reply = """Oh no, maybe try without Hard mode?"""
        else:
            reply = f"""Oh no, better luck next time. 😶‍🌫️
Surely you would have gotten it on the {stats_dict['guesses_needed']}th try! """

    return reply
