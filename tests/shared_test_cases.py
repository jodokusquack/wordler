test_cases = {
    'tc_success_1':
        """Wordle 1,715 4/6*

⬛️⬛️⬛️⬛️🟩
⬛⬛️⬛️⬛️🟩
⬛️🟨⬛️⬛️🟩
🟩🟩🟩🟩🟩""",

    'tc_success_2':
        """Wordle 1715 4/6

⬛️⬛️🟨⬛️⬛️
🟨⬛️⬛️⬛️🟨
🟩⬛️🟩🟩⬛️
🟩🟩🟩🟩🟩""",

    'tc_success_3':
        """Wordle 1713 5/6

⬜️⬜️⬜️⬜️🟨
⬜️🟨🟨🟨⬜️
⬜️🟩🟩🟨⬜️
⬜️🟩🟩🟩🟩
🟩🟩🟩🟩🟩""",

    'tc_success_4':
        """Wordle 1,713 2/6*

⬛️🟨⬛️⬛️🟨
🟩🟩🟩🟩🟩""",

    'tc_first_try':
        """Wordle 1702 1/6

🟩🟩🟩🟩🟩""",

    'tc_extra_text':
        """Look at my score:
Wordle 1,701 4/6

⬜️🟨⬜️⬜️🟨
⬜️⬜️🟨🟩⬜️
🟨⬜️🟨🟩⬜️
🟩🟩🟩🟩🟩

Its pretty good right? ♥️
""",

    'tc_wrong_text':
        """I solved it too:
it took me only 2/6 tries. I swear!""",

    'tc_fail_1':
        """Wordle 1.715 X/6

⬛⬛⬛⬛🟨
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛
🟩⬛⬛⬛⬛
⬛🟨⬛⬛⬛
⬛🟨⬛🟨⬛""",
}
