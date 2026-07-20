import json

from anthropic import Anthropic

from app.models.order import ParsedOrder

SYSTEM_MESSAGE = f"""\
You are a restaurant order parser. Extract every item the customer wants.

Respond with JSON matching this schema:
{json.dumps(ParsedOrder.model_json_schema(), indent=2)}

Return only valid JSON, no other text.\
"""


def parse_order(customer_text: str, client: Anthropic) -> ParsedOrder:
    """Call Claude once to extract a ParsedOrder from natural-language customer text."""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_MESSAGE,
        messages=[{"role": "user", "content": customer_text}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return ParsedOrder.model_validate_json(text)
