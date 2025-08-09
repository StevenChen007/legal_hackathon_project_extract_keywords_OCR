# Intelligent Assistance System for Benefit Applications
**Project Completed:** 09 August 2025

## 📌 Project Overview

This project aims to develop an **intelligent assistance system** that supports individuals applying for **non-repayable benefits** and **challenges unlawful sanctions**. It combines OCR (Optical Character Recognition) and AI chatbot technologies to process real-world data and extract meaningful patterns to train future models.

---

## 🧩 Problem Addressed

**Problem: Automated Benefit Application Tools**  
> Develop intelligent systems to assist individuals in applying for non-repayable assistance and challenge unlawful sanctions.

---

## 🗂️ Project Components

### 1. **OCR Scanned Document Pipeline**

- Physical benefit-related documents are first scanned and converted into `.docx` format.
- We use a Python script to:
  - Extract all text from the document
  - Split text into individual sentences
  - Check each sentence against a set of predefined key statements
  - Capture only those **sentences that contain more than one key statement**
  - Save the results into a **CSV file** and a **Wix database** for training

📄 Sample code:  
[Document Extraction Code](https://drive.google.com/file/d/1EO1uCOgBHbrka4ZoiglggE_VccotC6op/view?usp=sharing)

---

### 2. **AI Chatbot with Tinfoil API**

- The chatbot is developed using **Wix JavaScript backend functions** and connected to the **Tinfoil API**.
- The chatbot interacts with users and:
  - Captures **user questions**
  - Captures **AI responses** that contain more than one key statement
  - Stores both in a **Wix database** with timestamps
- These captured interactions serve as **training samples** for further automation and refinement of benefit application tools.

📄 Chatbot code:
- [Tinfoil API Chatbot Code](https://drive.google.com/file/d/1uZMPXOls1lGdh7t4rLoJ6i4HxW7q69K4/view?usp=sharing)
- [Wix Database Integration Code](https://drive.google.com/file/d/1ozX73KdMEG2UpnFTcARpDkxXzsoKng6Y/view?usp=sharing)

---

## 🗃️ Data Output

### ✔️ From OCR:
- Captured sentences with multiple key statements  
- Stored as `.csv` and sent to Wix collection

### ✔️ From Chatbot:
- Captured questions & responses meeting keyword criteria  
- Stored in the **ChatExtract** database  
  Sample schema:
  - `Question`
  - `Response`
  - `CreatedTime`

📄 Database example:  
[ChatExtract Sample](https://drive.google.com/file/d/1TdVLIJ69wHgAGPXoSjpir_WDL32ntpKY/view?usp=sharing)

---

## 🎯 Final Goal

The long-term aim is to use the high-quality data gathered from both:
- **OCR sentence extraction**
- **AI chatbot conversations**

…to train models capable of:
- Automatically filling out benefit applications
- Generating appeal letters
- Identifying sanction issues
- Recommending personalized advice for applicants

---

## 🚀 Technologies Used

- **Python** (text processing, sentence splitting, CSV output)
- **JavaScript + Wix Velo** (backend logic, API calls, database storage)
- **Tinfoil API** (AI-powered chatbot)
- **Wix CMS** (data storage and retrieval)

---

## 🔒 Ethical Considerations

- No personal or sensitive data is used.
- All inputs are anonymized or simulated for development.
- Data handling complies with GDPR and NZ Privacy Act standards.

---

## 🤝 Contributors

- Steven Chen
- University of Auckland

---

## 📬 Contact

For queries or collaboration, contact:  
📧 ste928014@gmail.com

---

