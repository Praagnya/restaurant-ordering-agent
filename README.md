# Voice AI Restaurant

An AI-powered restaurant ordering system that lets customers place orders via text, voice, or REST API. Powered by Claude for natural conversation and Deepgram for real-time speech processing.

## Features

- **Multi-modal ordering**: text (CLI), voice, and HTTP API
- **Natural language understanding**: Claude handles menu questions, modifications, and order confirmation
- **Voice pipeline**: real-time speech-to-text and text-to-speech with interruption support
- **PDF menu parsing**: upload a menu PDF to populate the system
- **Order persistence**: orders saved to JSON with timestamps
- **Observability**: LangSmith tracing integration

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Claude Sonnet (`claude-sonnet-4-5`) |
| Voice STT/TTS | Deepgram |
| Voice Activity Detection | Silero VAD |
| Voice pipeline | Pipecat |
| API framework | FastAPI |
| Data validation | Pydantic v2 |
| Tracing | LangSmith |
| Deployment | Docker + Fly.io |

## Project Structure

```
voice-ai-restaurant/
├── app/
│   ├── agent/          # Claude agent logic and tool definitions
│   ├── api/            # FastAPI app, routes, schemas, dependencies
│   ├── models/         # Pydantic models (cart, menu, order)
│   ├── repositories/   # Menu data and order persistence
│   └── services/       # Cart, menu search, PDF menu parser
├── tests/              # Unit tests
├── scripts/            # Utility scripts (e.g. parse_menu.py)
├── main.py             # CLI entry point
├── voice.py            # Voice interface entry point
└── Dockerfile
```

## Setup

### Prerequisites

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (package manager)

### Install dependencies

```bash
uv sync
```

### Environment variables

Create a `.env` file:

```env
ANTHROPIC_API_KEY=your_anthropic_key
DEEPGRAM_API_KEY=your_deepgram_key
LANGCHAIN_API_KEY=your_langsmith_key   # optional, for tracing
```

## Usage

### CLI (text-based)

```bash
python main.py
```

### Voice interface

```bash
python voice.py
```

### API server

```bash
uvicorn app.api.app:app --port 8080
```

#### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat` | Send a message and get an AI response |
| `GET` | `/menu` | Retrieve all menu items |
| `POST` | `/menu/parse` | Upload a PDF menu to populate the system |

## Deployment

The app is configured for [Fly.io](https://fly.io):

```bash
fly deploy
```

Configuration is in `fly.toml` (region: `iad`, 512 MB RAM, auto-scales to 0).

## Running Tests

```bash
pytest
```
