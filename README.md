# MedRelay AI CRM

<div align="center">

### AI-Powered Pharmaceutical CRM Assistant

Built using **React + FastAPI + LangGraph + Groq + SQLite**

<img src="https://img.shields.io/badge/React-Frontend-blue?style=for-the-badge&logo=react" />
<img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi" />
<img src="https://img.shields.io/badge/LangGraph-AI%20Workflow-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/Groq-LLM-red?style=for-the-badge" />
<img src="https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite" />

</div>

---

# Overview

MedRelay AI CRM is an intelligent healthcare interaction management system designed for pharmaceutical field representatives.

The platform uses **AI-powered agent workflows** to:

- Log doctor interactions
- Extract structured healthcare data
- Generate AI summaries
- Suggest follow-up actions
- Retrieve interaction history
- Manage healthcare professional engagement efficiently

The application integrates a **LangGraph multi-tool AI workflow** with a modern React dashboard and FastAPI backend.

---

# Features

## AI Interaction Logging
Automatically extracts:
- Doctor Name
- Hospital Name
- Specialty
- Interaction Type
- Notes
- Follow-Up Date

---

## LangGraph AI Workflow
Implements intelligent tool orchestration using:
- SummarizeInteractionTool
- FollowUpRecommendationTool
- LogInteractionTool
- InteractionHistoryTool
- EditInteractionTool

---

## Smart Recommendations
AI-generated follow-up suggestions for healthcare engagement.

---

## Interaction History
Retrieve previous doctor interactions instantly.

---

## Interaction Editing
Update existing interaction records using natural language.

---

## Modern Interactive Dashboard
Premium glassmorphism UI inspired by modern SaaS products.

---

# System Architecture

```text
Frontend (React + Tailwind)
            ↓
FastAPI Backend
            ↓
LangGraph Workflow Engine
            ↓
AI Tools + Groq LLM
            ↓
SQLite Database
```

---

# Tech Stack

| Technology | Purpose |
|---|---|
| React | Frontend UI |
| Tailwind CSS | Styling |
| FastAPI | Backend API |
| LangGraph | AI Workflow |
| Groq | LLM Integration |
| SQLite | Database |
| SQLAlchemy | ORM |
| Uvicorn | ASGI Server |

---

# Project Structure

```bash
medrelay-ai-crm/
│
├── medrelay-backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── medrelay-frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ Backend Setup

## 1️⃣ Navigate to backend

```bash
cd medrelay-backend
```

---

## 2️⃣ Create virtual environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Add Groq API Key

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

## 6️⃣ Run backend

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## 1️⃣ Navigate to frontend

```bash
cd medrelay-frontend
```

---

## 2️⃣ Install dependencies

```bash
npm install
```

---

## 3️⃣ Start frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# API Endpoint

## POST `/agent`

### Example Request

```json
{
  "message": "Met Dr Sharma at Ruby Hall Clinic. Interested in oncology drug samples."
}
```

---

## Example Response

```json
{
  "reply": "Interaction logged successfully",
  "summary": "Doctor interested in oncology samples",
  "recommendations": [
    "Schedule follow-up meeting"
  ],
  "tool_calls": [
    "SummarizeInteractionTool",
    "LogInteractionTool"
  ]
}
```

---

# LangGraph Workflow

The system uses a multi-step AI workflow:

```text
User Input
    ↓
Agent Node
    ↓
Tool Selection
    ↓
Tool Execution
    ↓
Database Storage
    ↓
AI Response
```

---

# 📸 Screenshots

## Dashboard
<img width="1892" height="923" alt="image" src="https://github.com/user-attachments/assets/7dabe790-52a6-47e4-890f-306fc28be343" />


---

## AI Interaction Logging

<img width="1912" height="918" alt="image" src="https://github.com/user-attachments/assets/178bbe1e-2ccc-4d57-9084-37931b1f3366" />



---

## Interaction History

<img width="1892" height="917" alt="image" src="https://github.com/user-attachments/assets/15be8499-1801-48d7-b74c-2c892ef75755" />


---


---

# Future Improvements

- Authentication System
- Advanced Analytics
- Multi-user Support
- Cloud Database
- Voice Interaction Logging
- AI Email Automation

---

# Author

### Purva Sonaje

AI/ML & Full Stack Developer

---

# Conclusion

MedRelay AI CRM demonstrates the integration of:

✅ Modern Frontend Engineering  
✅ FastAPI Backend Development  
✅ LangGraph AI Workflows  
✅ LLM Tool Orchestration  
✅ AI-powered Healthcare Automation  

This project showcases real-world AI application development for healthcare CRM systems.

---
