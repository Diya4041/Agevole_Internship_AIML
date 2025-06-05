
# 📄 AI Resume Screening Tool

An intelligent resume screening application built with **Streamlit** and **SpaCy** to automatically analyze resumes and match them with job descriptions using NLP techniques.

---

## 🚀 Features

- Upload and extract text from PDF and DOCX resumes
- Use NLP to analyze and compare resumes against job descriptions
- Generate match scores and insights
- Visualize results with clean, interactive UI

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install streamlit
pip install python-dotenv
pip install pdfplumber
pip install python-docx
pip install spacy
python -m spacy download en_core_web_sm
pip install scikit-learn
pip install matplotlib
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🛠 Tech Stack

- Python
- Streamlit
- spaCy
- scikit-learn
- matplotlib
- PDFPlumber
- python-docx
- dotenv

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
