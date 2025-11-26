# 📊 SQL Query AI Assistant
[![Live App](https://img.shields.io/badge/Live%20Demo-Streamlit%20App-brightgreen?style=for-the-badge&logo=streamlit)](https://harish-sql-query-ai-assistant.streamlit.app/)

SQL Query AI Assistant is a **Streamlit** application that converts **natural language questions** into **PostgreSQL queries** using Gemini/OpenAI.  
The app connects to a **Render-hosted PostgreSQL database**, executes the generated SQL, and shows results instantly.  
It is ideal for exploring **patients, admissions, diagnosis, and lab data** without manually writing SQL.

---

## ✨ Features

- 🤖 Natural language → SQL using Gemini / OpenAI  
- 🗄️ Executes queries against PostgreSQL (Render)  
- 🔗 Smart JOINs based on schema relationships  
- ⏱️ Automatic date/time functions & LIMIT handling  
- 🔐 Secure login using bcrypt hashed passwords  
- 🎨 Clean, modern dark UI with custom CSS  
- 📜 SQL history viewer and editable generated SQL  
- 📊 Interactive result tables  

---

## 📸 Screenshots (Add Yours)

| Login Screen | Query Generation | Query Execution |
| --- | --- | --- |
| <img src="https://github.com/user-attachments/assets/2bd4fcda-534a-4653-ad9d-e818d587ac58" width="300"/> | <img src="https://github.com/user-attachments/assets/b8430421-0236-4732-b96e-70f85d3aec86" width="300"/> | <img src="https://github.com/user-attachments/assets/df7ab29b-26d3-4c5b-a281-529fa7d803c5" width="300"/> |


---

## 🧠 Example Questions

### **Demographics**
- How many patients do we have by gender?  
- What is the average age by race?

### **Admissions**
- What is the average length of stay?  
- Which 10 patients have the most admissions?

### **Labs**
- What are the top 10 most common lab tests?  
- Show all labs for patient `1A8791E3-A61C-455A-8DEE-763EB90C9B2C`  
- What is the average METABOLIC: SODIUM value?

---

## 🗄️ Supporting Services

- 🟣 **PostgreSQL (Render.com)** — hosted database  
- 🤖 **Gemini / OpenAI** — SQL generation  
- 🎈 **Streamlit Community Cloud** — optional hosting  
- 🔒 Local `.env` or Streamlit Secrets for secure credentials  

---

## ⚙️ Local Setup (Development)

```bash
# 1️⃣ Clone the Repository
git clone https://github.com/harish-334/sql-query-ai-assistant.git
cd sql-query-ai-assistant

# 2️⃣ Create .env File (rename sample.env → .env and fill the values)
# Required fields:
# OPENAI_API_KEY=your_api_key
# POSTGRES_USERNAME=your_user
# POSTGRES_PASSWORD=your_pass
# POSTGRES_SERVER=your_render_host
# POSTGRES_DATABASE=your_db
# HASHED_PASSWORD=your_bcrypt_hash

# 3️⃣ Create & Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux

# 4️⃣ Install Dependencies
pip install -r requirements.txt

# 5️⃣ Generate Hashed Password (for login)
python generate_password.py

# OR manual hashing:
# import bcrypt
# password = "some_strong_password".encode('utf-8')
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# print(hashed.decode())

# 6️⃣ Test DB Connection
python test_render_database.py

# 7️⃣ (Optional) Populate Database Tables
python populate_db.py

## 8️⃣ Run the Streamlit Application
streamlit run streamlit_app.py
```

---

## ☁️ Deploy on Streamlit Community Cloud

```bash
# 1️⃣ Push project to GitHub
git add .
git commit -m "Deploy Streamlit AI SQL Assistant"
git push origin main

# 2️⃣ Go to Streamlit Cloud
# https://share.streamlit.io

# 3️⃣ Create New App:
# Repo: harish-334/sql-query-ai-assistant
# Branch: main
# File: streamlit_app.py

# 4️⃣ Add Secrets
# OPENAI_API_KEY=your_api_key
# POSTGRES_USERNAME=your_user
# POSTGRES_PASSWORD=your_pass
# POSTGRES_SERVER=your_render_host
# POSTGRES_DATABASE=your_db
# HASHED_PASSWORD=your_bcrypt_hash

# 5️⃣ Deploy → Streamlit builds + installs + launches automatically
# Live App: https://harish-sql-query-ai-assistant.streamlit.app/
```

---

## 📁 Project Structure

```pgsql
query_patients/
├── streamlit_app.py
├── populate_db.py
├── test_render_database.py
├── generate_password.py
├── requirements.txt
├── .env (local only - DO NOT COMMIT)
├── .streamlit/config.toml
├── AdmissionsCorePopulatedTable.txt
├── AdmissionsDiagnosesCorePopulatedTable.txt
├── LabsCorePopulatedTable.txt
├── PatientCorePopulatedTable.txt
└── README.md
```

## 📄 License
- For academic and educational use only.

## ✉️ Contact
- For feedback or questions, reach out at: harishsondagar3@gmail.com
