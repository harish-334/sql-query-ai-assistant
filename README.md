# 📊 SQL Query AI Assistant  
[![Live App](https://img.shields.io/badge/Live%20Demo-Streamlit%20App-brightgreen?style=for-the-badge&logo=streamlit)](https://harish-sql-query-ai-assistant.streamlit.app/)

An AI-powered **natural-language → SQL** assistant built with **Streamlit**, **Gemini**, and a **PostgreSQL + SQLite hybrid backend**.  
Ask questions in English about **patient data** or **normalized e-commerce data**, and the app generates **PostgreSQL-ready SQL** automatically with accurate table/column quoting, JOINs, grouping, timestamps, and more.

---

## ✨ Features

- 🤖 Convert natural language questions into **PostgreSQL queries**
- 🧠 Strong SQL generation rules (quoted identifiers, correct schemas)
- 🗄️ Auto-detect DB engine  
  - Uses **Postgres (Render)**  
  - Or **SQLite (`normalized.db`)** automatically if available
- 🔗 JOIN-aware SQL based on schema
- 🔐 Secure login using bcrypt hashed passwords
- 📜 Query history + editable SQL + instant results
- ⚡ Fast Streamlit UI with simple workflow
- 🌍 Supports **two full datasets**:
  - Healthcare (patients, admissions, labs)
  - E-commerce normalized DB (Customer, Product, OrderDetail, Region, Country)

---

## 🧠 Example Questions

### **🧍 Patient Demographics**
- How many patients do we have by gender?
- What is the average age by race?
- Count patients by language.
- Show the average poverty % by marital status.

### **🏥 Admissions**
- What is the average length of stay?
- Which patients have the most admissions?
- Show admissions grouped by month.

### **🧪 Lab Results**
- Show the latest lab for each patient.
- What are the top 10 most common lab tests?
- Show glucose trend over time.

---

## 🛒 E-Commerce / Normalized DB

### 🌍 Region & Country
- Count countries per region.
- Show customer count per region.

### 🧑‍💼 Customers
- Show top 10 customers by total spending.
- List customers from United States.
- Count customers by country.

### 📦 Products & Categories
- Show top 10 most expensive products.
- List all products under “Beverages”.
- Count products per category.

### 🧾 Orders / Sales
- Total quantity ordered per product.
- Top 10 customers by order quantity.
- Revenue per product category.
- Daily sales trends.

---

## ⚙️ Local Setup (Development)

1️⃣ Clone repository
git clone https://github.com/harish-334/sql-query-ai-assistant.git
cd sql-query-ai-assistant

2️⃣ Create .env file with:
OPENAI_API_KEY=
POSTGRES_USERNAME=
POSTGRES_PASSWORD=
POSTGRES_SERVER=
POSTGRES_DATABASE=
HASHED_PASSWORD=

3️⃣ Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the app locally
streamlit run streamlit_app.py

---

## ☁️ Deploy on Streamlit Cloud
Push code to GitHub
git add .
git commit -m "Deploy updated SQL AI Assistant"
git push origin main

Then:
Open https://share.streamlit.io

Create new app:

Repo: harish-334/sql-query-ai-assistant
Branch: main
File: streamlit_app.py

Add Streamlit Secrets:

OPENAI_API_KEY=

POSTGRES_USERNAME=

POSTGRES_PASSWORD=

POSTGRES_SERVER=

POSTGRES_DATABASE=

HASHED_PASSWORD=



Click Deploy ✔
The app auto-builds and launches.

---
## 📁 Project Structure
```bash
query_patients/
│
├── streamlit_app.py               # Main Streamlit app
├── requirements.txt               # Python dependencies
├── normalized.db                  # Optional local SQLite DB
│
├── migrate_sqlite_to_postgres.py
├── add_primary_keys.py
├── add_fks_safe_v2.py
├── check_parent_keys.py
│
├── test_sql_query.py
├── test_sqlite_db.py
├── verify_postgres.py
│
├── .env (ignored)
└── .streamlit/config.toml
```
---

## 📄 License
Free for educational and academic use.

---
## ✉️ Contact
📩 harishsondagar3@gmail.com | harishha@buffalo.edu

---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/af049c9a-f7fa-47cd-997f-019ddea555a0" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/af33e5e3-7982-4a05-84cd-9dc22720fe35" />
