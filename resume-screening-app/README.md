
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

---

## 🔥 Firebase Setup (Optional - For Cloud Integration)

To enable Firebase integration for storing user data, logs, or reports:

### 1. Set Up Firebase Project

- Go to [Firebase Console](https://console.firebase.google.com/)
- Create a new project
- Navigate to **Project Settings > Service Accounts**
- Click **Generate new private key** and download the `.json` file

### 2. Add Environment Variables

Create a `.env` file in your project root and add the following:

```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxx@your-project-id.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nABCDEF...\n-----END PRIVATE KEY-----\n"
```

> ⚠️ Escape newlines in your private key using `\n`

### 3. Install Firebase Admin SDK

```bash
pip install firebase-admin
```

### 4. Initialize Firebase in your Code

Example initialization:

```python
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    ...
})

firebase_admin.initialize_app(cred)
```
