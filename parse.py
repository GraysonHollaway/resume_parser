import tkinter as tk
from tkinter import filedialog
import PyPDF2
import docx
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def parse_job_description(job_description):
    # Tokenize the job description and remove punctuation
    words = re.findall(r'\b\w+\b', job_description.lower())
    return Counter(words)

def match_words(job_text, document_text):
    job_word_count = parse_job_description(job_text)
    document_word_count = Counter(re.findall(r'\b\w+\b', document_text.lower()))
    
    # Get English stop words
    stop_words = set(stopwords.words('english'))

    matched_words = {}
    for word, count in document_word_count.items():
        if word not in stop_words and word in job_word_count:
            matched_words[word] = count
    
    return matched_words

def browse_file():
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def analyze_document():
    file_path = entry.get()
    if file_path.endswith('.pdf'):
        document_text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        document_text = extract_text_from_docx(file_path)
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Unsupported file format. Please select a PDF or DOCX file.")
        return

    matched_words = match_words(job_description_text.get(1.0, tk.END), document_text)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Matched words:\n")
    for word, count in matched_words.items():
        result_text.insert(tk.END, f"{word}: {count}\n")

# Create the main window
root = tk.Tk()
root.title("Job Match Analyzer")

# Create and arrange widgets
label1 = tk.Label(root, text="Select a PDF or DOCX file:")
label1.pack()

entry = tk.Entry(root, width=50)
entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

label2 = tk.Label(root, text="Paste the job description here:")
label2.pack()

job_description_text = tk.Text(root, height=10, width=50)
job_description_text.pack()

analyze_button = tk.Button(root, text="Analyze Document", command=analyze_document)
analyze_button.pack()

result_text = tk.Text(root, height=20, width=50)
result_text.pack()

# Start the GUI event loop
root.mainloop()