def main():
   #key_statements = ["income", "sanction", "initiative", "benefits", "appeal", "support"]
    text = extract_text_from_docx("example.docx")
    # Define key statements to look for in the text (to be modified as needed)
    extraction = extract_key_statements(text).split('\n')
    save_to_csv(extraction, "test1.csv")
    import_to_db(extraction, "key_statements.db")


# Print all the sentences from OCR scanned document, to be used for further processing.
from docx import Document

def extract_text_from_docx(doc_file):
    doc = Document(doc_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

#print(text)


# Extract sentences with more than key statement from the text
import re
def extract_key_statements(text):
    # Define key statements to look for in the text (to be modified as needed)
    key_statements = ["income", "sanction", "initiative", "benefits", "appeal", "support"]

    # Regular expression to match key statements
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    matches = []
    for sen in sentences:
        lower_sen = sen.lower()
        found = [statement for statement in key_statements if statement in lower_sen]
        if len(found) > 1: #  Find sentences with more than one key statement
            matches.append(sen.strip())
    return '\n'.join(matches)

#print(extract_key_statements(text))

# Save the extracted key statements to a csv file
import pandas as pd
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=["Key Statements"])
    df.to_csv(filename, index=False)
#save_to_csv(extract_key_statements(text).split('\n'), "test1.csv")

# Import the extracted key statements into a Database
import sqlite3
def import_to_db(data, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS key_statements (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   statement TEXT UNIQUE)
                   ''')
    
    for statement in data:
        cursor.execute('INSERT OR IGNORE INTO key_statements (statement) VALUES (?)', (statement,))
        # Check if the statement already exists to avoid duplicates
    
    conn.commit()
    conn.close()

#import_to_db(extract_key_statements(text).split('\n'), "key_statements.db")

# Print the extracted key statements to check the database
import sqlite3

def print_extracted_statements(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM key_statements')  # id and sentence
    rows = cursor.fetchall()
    for row in rows:
        print(row[1])  # row[0] is id, row[1] is the sentence
    conn.close()

if __name__ == "__main__":
    main()
    print_extracted_statements("key_statements.db")
    # This will print all the extracted key statements from the database
