import asyncio
import uuid

from fastapi import APIRouter

from app.agent.agent import run_agent
from app.api.dependencies import Session, client, menu, sessions
from app.api.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # Create new session if none provided
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = Session()

    session = sessions[session_id]

    response_text, session.cart, session.messages = await asyncio.to_thread(
        run_agent,
        request.message,
        client,
        menu,
        session.cart,
        session.messages,
    )

    return ChatResponse(
        session_id=session_id,
        response=response_text,
        cart=session.cart,
    )
