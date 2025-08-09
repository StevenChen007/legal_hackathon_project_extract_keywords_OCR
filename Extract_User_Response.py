import requests
import pandas as pd
import sqlite3
import re
import os

API_URL = "https://inference.tinfoil.sh/v1/chat/completions"
API_KEY = "tk_rBPwBFh33OE2uF2oQJUCm2rOSjalOcKT6WkeXp91mLDKpii0"

def get_bot_response(user_question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-3-70b",
        "messages": [{"role": "user", "content": user_question}]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Tinfoil API error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

def extract_key_statements(response):
    keywords = ["sustainability", "goal", "climate", "carbon", "environment", "benefits", "support"]
    sentences = re.split(r'(?<=[.!?])\s+', response)
    key_statements = [s.strip() for s in sentences if any(k in s.lower() for k in keywords)]
    return " | ".join(key_statements)

def get_existing_questions_from_db(db_name):
    if not os.path.exists(db_name):
        return set()
    conn = sqlite3.connect(db_name)
    try:
        query = "SELECT question FROM chat_responses"
        df = pd.read_sql_query(query, conn)
        return set(df["question"].str.strip())
    except Exception:
        return set()
    finally:
        conn.close()

def save_to_excel_append(data, filename):
    try:
        existing_df = pd.read_excel(filename)
        existing_questions = set(existing_df["question"].str.strip())
    except FileNotFoundError:
        existing_df = pd.DataFrame()
        existing_questions = set()

    new_df = pd.DataFrame(data)
    new_df = new_df[~new_df["question"].str.strip().isin(existing_questions)]

    final_df = pd.concat([existing_df, new_df], ignore_index=True)
    final_df.to_excel(filename, index=False)
    print(f"Excel updated: {filename}")

def save_to_sqlite_append(data, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_responses (
            id INTEGER,
            question TEXT UNIQUE,
            key_statements TEXT
        )
    ''')

    for row in data:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO chat_responses (id, question, key_statements)
                VALUES (?, ?, ?)
            ''', (row["id"], row["question"].strip(), row["key_statements"]))
        except Exception as e:
            print("Error inserting row:", e)

    conn.commit()
    conn.close()
    print(f"Database updated: {db_name}")

def main():
    user_questions = [
        "What are the sustainability goals of your company?",
        "How do you reduce carbon emissions?",
        "Tell me about your recycling initiatives.",
        "What are your core business services?",
        "How can customers contact your support team?"
    ]

    db_name = "test_extract_response.db"
    excel_file = "test_extract_response.xlsx"
    existing_questions = get_existing_questions_from_db(db_name)

    dataset = []
    for idx, question in enumerate(user_questions, start=1):
        if question.strip() in existing_questions:
            print(f"Skipped duplicate: {question}")
            continue

        print(f"Processing Q{idx}: {question}")
        try:
            response = get_bot_response(question)
            key_statements = extract_key_statements(response)
            if key_statements:
                dataset.append({
                    "id": idx,
                    "question": question,
                    "key_statements": key_statements
                })
            else:
                print(f"No key statements found for Q{idx}")
        except Exception as e:
            print(f"Error processing Q{idx}: {e}")

    if dataset:
        save_to_excel_append(dataset, excel_file)
        save_to_sqlite_append(dataset, db_name)
    else:
        print("No new responses to save.")

def read_key_statements_from_db(db_name="test_extract_response.db"):
    conn = sqlite3.connect(db_name)
    try:
        query = "SELECT id, question, key_statements FROM chat_responses"
        df = pd.read_sql_query(query, conn)
        print("Key statements retrieved from database:")
        print(df)
        return df
    except Exception as e:
        print("Error reading from database:", e)
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    main()
    read_key_statements_from_db("test_extract_response.db")
