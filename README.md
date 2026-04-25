# Grid07 - AI Cognitive Engine

This project implements the Grid07 AI Engineering Assignment: Cognitive Routing and RAG.

## What Is Implemented

- Phase 1: Vector-based persona matching router using local embeddings + in-memory ChromaDB.
- Phase 2: LangGraph autonomous content engine with a mock search tool and strict structured outputs.
- Phase 3: Deep-thread combat engine with RAG-style thread context and prompt-injection defense.

## Tech Stack

- Python 3.12
- FastAPI
- LangChain + LangGraph
- ChromaDB (in-memory)
- sentence-transformers (all-MiniLM-L6-v2)
- Groq (or fallback mode if no API key)

## Repository Structure

- backend/: FastAPI app and all assignment phases
- frontend/: Next.js UI for router, engine, and combat demos
- logs/: execution logs for each assignment phase

## Phase 1 - Vector Persona Router

Core function: `route_post_to_bots(post_content: str, threshold: float = 0.85)`

Implementation summary:
- Three bot personas are embedded and stored in an in-memory ChromaDB collection.
- Incoming post text is embedded with the same embedding model.
- Similarity search is done with cosine distance, converted to similarity as `1 - distance`.
- Only bots above threshold are returned as matches.

Key files:
- backend/phase1/embedder.py
- backend/phase1/vector_store.py
- backend/phase1/router.py
- backend/personas/bots.py

## Phase 2 - LangGraph Autonomous Content Engine

Graph structure:
- START -> `decide_search` -> `web_search` -> `draft_post` -> END

Node behavior:
- decide_search: Uses persona text to choose a topic and search query.
- web_search: Calls `mock_searxng_search(query)` to retrieve recent hardcoded headlines.
- draft_post: Uses persona + search context to generate a 280-char opinionated post.

Strict JSON guarantee:
- Structured outputs are enforced with Pydantic schemas via `with_structured_output(...)`.
- Final shape is always validated as:
	- `bot_id`
	- `topic`
	- `post_content`

Key files:
- backend/phase2/tools.py
- backend/phase2/nodes.py
- backend/phase2/graph.py
- backend/phase2/engine.py

## Phase 3 - Combat Engine (Deep Thread RAG)

Core function: `generate_defense_reply(bot_id, parent_post, comment_history, human_reply)`

RAG prompt strategy:
- Parent post and full comment history are formatted into a single thread context block.
- The model gets system instructions (persona + identity lock) and user message (latest reply).
- Reply is grounded in the full argument context, not just the last message.

Prompt injection defense strategy:
- Injection heuristics (`detect_injection_attempt`) flag common override patterns.
- System-level identity lock marks persona as immutable and rejects role-change attempts.
- If an attack appears, the bot stays in character and continues debating.

Key files:
- backend/phase3/prompt_builder.py
- backend/phase3/injection_guard.py
- backend/phase3/combat.py

## API Endpoints

- POST `/api/phase1/route`
- POST `/api/phase2/generate`
- POST `/api/phase3/defend`
- GET `/api/health`

## Local Setup

1. Create and activate virtual environment.
2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp ../.env.example ../.env
```

4. Run backend:

```bash
uvicorn main:app --reload
```

5. Run tests:

```bash
cd backend
pytest -q
```

## Deliverables Included

- Python implementation for all three phases in backend/
- requirements file: backend/requirements.txt
- environment template: .env.example
- execution logs:
	- logs/phase1_execution.md
	- logs/phase2_execution.md
	- logs/phase3_execution.md
