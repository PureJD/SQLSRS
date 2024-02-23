import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect('srs_database.db')
c = conn.cursor()

# Create table to store items
c.execute('''CREATE TABLE IF NOT EXISTS items
             (id INTEGER PRIMARY KEY, question TEXT, answer TEXT, last_reviewed DATE, next_review_date DATE)''')

# Function to add item to database
def add_item():
    question = question_entry.get()
    answer = answer_entry.get()
    today = datetime.date.today()
    next_review_date = today + datetime.timedelta(days=1)  # Initial review tomorrow
    c.execute("INSERT INTO items (question, answer, last_reviewed, next_review_date) VALUES (?, ?, ?, ?)",
              (question, answer, today, next_review_date))
    conn.commit()
    messagebox.showinfo("Success", "Item added successfully!")

# Function to retrieve the next item due for review
def get_next_item():
    today = datetime.date.today()
    c.execute("SELECT * FROM items WHERE next_review_date <= ? ORDER BY next_review_date ASC LIMIT 1", (today,))
    return c.fetchone()

# Function to update the review status of an item
def update_item(correct):
    item = get_next_item()
    if item:
        today = datetime.date.today()
        next_review_date = today + datetime.timedelta(days=1) if correct else today  # Retry tomorrow if correct, else retry today
        c.execute("UPDATE items SET last_reviewed = ?, next_review_date = ? WHERE id = ?",
                  (today, next_review_date, item[0]))
        conn.commit()
        messagebox.showinfo("Success", "Review status updated successfully!")
    else:
        messagebox.showinfo("No Items", "No items to review!")

# Function to display all items in the database
def see_all_items():
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    items_text = ""
    for item in items:
        items_text += f"ID: {item[0]}\nQuestion: {item[1]}\nAnswer: {item[2]}\nLast Reviewed: {item[3]}\nNext Review Date: {item[4]}\n\n"
    messagebox.showinfo("All Items", items_text)

# Create main application window
root = tk.Tk()
root.title("Spaced Repetition System")
root.configure(background='black')

# Create and place widgets
question_label = tk.Label(root, text="Question:")
question_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
question_label.configure(background='black', foreground='green')
question_entry = tk.Entry(root)  # Set height to 2 lines
question_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="we")  # Set columnspan to 2
question_entry.configure(background='black', foreground='green')

answer_label = tk.Label(root, text="Answer:")
answer_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
answer_label.configure(background='black', foreground='green')
answer_entry = tk.Entry(root)  # Set height to 2 lines (default width is fine)
answer_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
answer_entry.configure(background='black', foreground='green')

add_button = tk.Button(root, text="Add Item", command=add_item)
add_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nswe")
add_button.configure(background='black', foreground='black')
add_button.configure(highlightbackground='black')

review_button = tk.Button(root, text="Review Item", command=lambda: update_item(correct=True))
review_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nswe")
review_button.configure(background='black', foreground='black')
review_button.configure(highlightbackground='black')

see_all_button = tk.Button(root, text="See All Items", command=see_all_items)
see_all_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nswe")
see_all_button.configure(background='black', foreground='black')
see_all_button.configure(highlightbackground='black')

# Start the GUI main loop
root.mainloop()
