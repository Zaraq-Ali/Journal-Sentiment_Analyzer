# Journal-Sentiment_Analyzer

A desktop application built with **Python** and **Tkinter** that analyzes the **sentiment** of journal entries using **Hugging Face Transformers**. It helps users track their emotional well-being over time by saving, classifying, and filtering journal entries by date and sentiment type.

---

##  Features

 **Sentiment Analysis** (Positive/Negative) on a per-sentence level  
 **GUI** with an intuitive interface (Tkinter)  
 **Calendar date picker** to select and filter entries  
 **Searchable journal history** with filters by **date** and **sentiment type**  
 **Auto-save** journal entries with timestamps and sentiment scores  
 Lightweight and easy to run locally — no internet required after install  

---

## Technologies Used
-  Python 3.11+
-  Tkinter (GUI framework)
-  Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`)
-  NLTK (sentence tokenization)
-  SQLite (local storage)
-  `tkcalendar` (for calendar widget)

---

## How It Works
1. User writes a journal entry in the text box.
2. Each sentence is classified using a transformer-based sentiment model.
3. The app displays:
   - Individual sentence sentiment (POSITIVE / NEGATIVE)
   - Overall average sentiment score
4. The entry is saved to a local SQLite database.
5. Users can later:
   - Filter entries by date (calendar)
   - Filter by sentiment (Positive / Negative / All)
