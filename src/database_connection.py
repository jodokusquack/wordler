import os
import sqlite3

# Env variables
database_path = os.getenv("DATABASE_PATH")


# --- DATABASE SETUP ---
def init_db():
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS wordles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    timestamp TEXT,
                    wordle_id INTEGER,
                    hard_mode BOOLEAN,
                    solved BOOLEAN,
                    guesses_needed INTEGER,
                    guesses TEXT
                    )
                    ''')
        conn.commit()


def save_wordle(
        user_id: int,
        username: str,
        timestamp: str,
        wordle_id: int,
        hard_mode: bool,
        solved: bool,
        guesses_needed: int,
        guesses: str) -> None:
    """Save a result to the wordles table."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO wordles (user_id, username, timestamp, wordle_id, hard_mode, solved, guesses_needed, guesses) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, timestamp, wordle_id, hard_mode, solved, guesses_needed, guesses)
        )
        conn.commit()


def extract_stats(user_id: int, include_unsolved: bool) -> dict:
    """Extract some stats for a user."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # define query with ? to prevent sql injection
        if include_unsolved:
            query = "SELECT guesses_needed FROM wordles WHERE user_id = ?"
        else:
            query = "SELECT guesses_needed FROM wordles WHERE user_id = ? AND solved = 1"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        guess_list = [row[0] for row in results]

    stats = {
        'guess_list': guess_list,
        'no_of_guesses': len(guess_list),
        'total_number_of_guesses': sum(guess_list),
        'average_score': sum(guess_list) / len(guess_list)
    }

    return stats


def check_user_exists(user_id: int) -> bool:
    """Check if a specific user already has an entry in the database."""
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM wordles WHERE user_id = ?)"
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

    results = [row[0] for row in results]
    exists = bool(results[0])
    return exists
