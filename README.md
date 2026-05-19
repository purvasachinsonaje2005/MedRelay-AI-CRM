# MedRelay AI CRM

## Overview
AI-powered pharmaceutical CRM assistant for healthcare interactions.

## Features
- AI interaction logging
- LangGraph multi-tool workflow
- Interaction history retrieval
- Follow-up recommendations
- Structured doctor data extraction
- FastAPI backend
- React frontend

## Tech Stack
- React
- Tailwind CSS
- FastAPI
- LangGraph
- Groq
- SQLite
- SQLAlchemy

## Architecture
Frontend → FastAPI → LangGraph → AI Tools → Database

## Setup Instructions

### Backend
cd medrelay-backend
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend
cd medrelay-frontend
npm install
npm run dev

## API Endpoints
- POST /agent
- GET /docs

## Demo
(Add screenshots here)
