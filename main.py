import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
from datetime import datetime
from tkcalendar import DateEntry
import os

# Download tokenizer
nltk.download('punkt')

# Load sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    sentences = sent_tokenize(text)
    results = []
    for sent in sentences:
        res = sentiment_pipeline(sent)[0]
        results.append((sent, res['label'], res['score']))
    return results

def save_to_file(text, results, avg_score, overall_sentiment):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("journal_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n=== Journal Entry ({timestamp}) ===\n")
        f.write(text + "\n\n")
        f.write(f"Overall Sentiment: {overall_sentiment} ({avg_score:.3f})\n")
        for sentence, label, score in results:
            f.write(f"{label:>8} ({score:.2f}) → {sentence}\n")
        f.write("="*40 + "\n")

def search_by_date_and_sentiment():
    search_date = date_picker.get()
    selected_sentiment = sentiment_filter.get().upper()

    if not os.path.exists("journal_log.txt"):
        messagebox.showinfo("No History", "No journal history found.")
        return

    try:
        with open("journal_log.txt", "r", encoding="utf-8") as f:
            logs = f.read().split("========================================")

        matches = []
        for log in logs:
            if search_date in log:
                if selected_sentiment == "ALL" or f"Overall Sentiment: {selected_sentiment}" in log:
                    matches.append(log.strip())

        result_display.delete("1.0", tk.END)
        if matches:
            for entry in matches:
                result_display.insert(tk.END, entry + "\n" + "-"*60 + "\n")
        else:
            result_display.insert(tk.END, f"No entries found for {search_date} with sentiment: {selected_sentiment}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def analyze_entry():
    text = entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input needed", "Please enter your journal.")
        return

    try:
        results = analyze_sentiment(text)
        avg_score = sum(+s if l == "POSITIVE" else -s for _, l, s in results) / len(results)
        overall_sentiment = "POSITIVE" if avg_score >= 0 else "NEGATIVE"

        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Overall Sentiment: {overall_sentiment} ({avg_score:.3f})\n\n")
        for sentence, label, score in results:
            output.insert(tk.END, f"{label:>8} ({score:.2f}) → {sentence}\n")

        save_to_file(text, results, avg_score, overall_sentiment)
        messagebox.showinfo("Saved", "Journal and sentiment saved to journal_log.txt")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- GUI Layout ----------------
root = tk.Tk()
root.title("Journal Sentiment Analyzer")
root.geometry("1200x600")

# Left Frame - Entry and Output
journal_frame = tk.Frame(root)
journal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(journal_frame, text="Enter your journal entry:", font=("Arial", 12)).pack()
entry = scrolledtext.ScrolledText(journal_frame, wrap=tk.WORD, width=80, height=10, font=("Arial", 11))
entry.pack(pady=5)

analyze_btn = tk.Button(journal_frame, text="Analyze Sentiment", command=analyze_entry,
                        font=("Arial", 12), bg="#4CAF50", fg="white")
analyze_btn.pack(pady=5)

output = scrolledtext.ScrolledText(journal_frame, wrap=tk.WORD, width=80, height=15, font=("Consolas", 10))
output.pack(pady=5)

# Right Frame - History Search
history_frame = tk.Frame(root)
history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(history_frame, text="Pick a Date to Search History:", font=("Arial", 12)).pack()
date_picker = DateEntry(history_frame, width=18, font=("Arial", 12), date_pattern='yyyy-mm-dd')
date_picker.pack(pady=5)

tk.Label(history_frame, text="Filter by Sentiment:", font=("Arial", 12)).pack(pady=(10, 0))
sentiment_filter = ttk.Combobox(history_frame, values=["All", "Positive", "Negative"], state="readonly")
sentiment_filter.set("All")
sentiment_filter.pack(pady=5)

search_btn = tk.Button(history_frame, text="Search", command=search_by_date_and_sentiment,
                       font=("Arial", 11), bg="#2196F3", fg="white")
search_btn.pack(pady=5)

result_display = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, width=50, height=30, font=("Consolas", 10))
result_display.pack(pady=5)

# Run app
root.mainloop()
