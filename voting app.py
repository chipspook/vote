
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def initialize_database():
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE,
            candidate_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_vote_to_db(voter_id: str, candidate_name: str) -> bool:
    """
    Saves the voter's ID and their selected candidate to the database.

    Args:
        voter_id (str): Unique identifier of the voter.
        candidate_name (str): Name of the selected candidate.

    Returns:
        bool: True if the vote was saved successfully, False if there was a duplicate voter ID.
    """
    conn = sqlite3.connect('voting.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO votes (voter_id, candidate_name) VALUES (?, ?)', (voter_id, candidate_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_voter_id(voter_id: str) -> bool:
    """
    Validates the voter ID to ensure it meets the required criteria.

    Args:
        voter_id (str): The voter ID to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return len(voter_id) >= 5 and voter_id.isalnum()

def submit_vote(voter_id, candidate, result_label):
    if not validate_voter_id(voter_id):
        messagebox.showerror("Invalid Voter ID", "Voter ID must be at least 5 alphanumeric characters.")
        return

    success = save_vote_to_db(voter_id, candidate)
    if success:
        result_label.config(text=f"Vote recorded for {candidate}!", fg="green")
    else:
        messagebox.showerror("Duplicate Vote", "This voter ID has already been used.")

def main():
    initialize_database()

    root = tk.Tk()
    root.title("Voting App")

    tk.Label(root, text="Enter Your Voter ID:").grid(row=0, column=0, padx=10, pady=10)
    voter_id_entry = tk.Entry(root)
    voter_id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Choose a Candidate:").grid(row=1, column=0, padx=10, pady=10)

    candidates = ["Bianca", "Edward", "Felicia"]
    candidate_var = tk.StringVar(value=candidates[0])

    candidate_menu = tk.OptionMenu(root, candidate_var, *candidates)
    candidate_menu.grid(row=1, column=1, padx=10, pady=10)

    result_label = tk.Label(root, text="", fg="green")
    result_label.grid(row=3, column=0, columnspan=2, pady=10)

    submit_button = tk.Button(
        root,
        text="Submit Vote",
        command=lambda: submit_vote(voter_id_entry.get(), candidate_var.get(), result_label)
    )
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

