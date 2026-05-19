# MedRelay — FastAPI + LangGraph + Groq backend (starter)

This is the local backend that pairs with the MedRelay React frontend.
It exposes REST endpoints for HCP interaction CRUD and an `/agent`
endpoint that runs a LangGraph workflow powered by Groq's
`gemma2-9b-it` model.

## Stack

- **FastAPI** — REST API
- **SQLAlchemy + SQLite** — local persistence (file: `medrelay.db`)
- **LangGraph** — agent orchestration with 5 tools:
  `LogInteractionTool`, `EditInteractionTool`, `SummarizeInteractionTool`,
  `FollowUpRecommendationTool`, `InteractionHistoryTool`
- **Groq** — `gemma2-9b-it` LLM via `langchain-groq`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and paste your GROQ_API_KEY (https://console.groq.com/keys)

uvicorn app.main:app --reload --port 8000
```

API will be at `http://localhost:8000`. Interactive docs at `/docs`.

## Environment variables

```
GROQ_API_KEY=gsk_...
GROQ_MODEL=gemma2-9b-it
DATABASE_URL=sqlite:///./medrelay.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Endpoints

| Method | Path                       | Description                          |
|--------|----------------------------|--------------------------------------|
| GET    | `/interactions`            | List interactions                    |
| POST   | `/interactions`            | Create interaction                   |
| GET    | `/interactions/{id}`       | Get one                              |
| PATCH  | `/interactions/{id}`       | Update                               |
| DELETE | `/interactions/{id}`       | Delete                               |
| POST   | `/agent`                   | Run LangGraph agent on a user message|

### `/agent` request

```json
{ "message": "Met Dr Sharma today at Ruby Hall Clinic. Discussed diabetes medicine. Follow-up next Tuesday." }
```

### `/agent` response

```json
{
  "reply": "Logged the interaction. Suggested follow-ups: ...",
  "draft": { "doctor_name": "Dr. Sharma", "hospital_name": "Ruby Hall Clinic", ... },
  "summary": "...",
  "recommendations": ["..."],
  "tool_calls": ["LogInteractionTool", "FollowUpRecommendationTool"]
}
```

## Wiring to the React frontend

In `src/lib/mockAgent.ts` of the frontend, replace `runAgent` with:

```ts
export async function runAgent(message: string) {
  const r = await fetch("http://localhost:8000/agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return r.json();
}
```

And for the CRUD operations, replace the Redux localStorage persistence
with `fetch("http://localhost:8000/interactions")` calls.

## Project structure

```
backend/
├── app/
│   ├── main.py            # FastAPI app & CORS
│   ├── database.py        # SQLAlchemy engine/session
│   ├── models.py          # Interaction ORM model
│   ├── schemas.py         # Pydantic request/response models
│   ├── crud.py            # DB helpers
│   ├── routes.py          # /interactions REST routes
│   └── agent/
│       ├── graph.py       # LangGraph workflow
│       ├── tools.py       # 5 agent tools
│       └── llm.py         # Groq client
├── requirements.txt
├── .env.example
└── README.md
```
