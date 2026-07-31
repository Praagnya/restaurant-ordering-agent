import base64
import mimetypes

from anthropic import Anthropic

SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

EXTRACTION_PROMPT = """Extract every menu item from this restaurant menu.

Rules:
- Include every item visible on the menu, across all sections
- Use empty string for missing descriptions
- Convert prices to cents as an integer (e.g. $5.99 → 599, $27 → 2700)
- Set available to true unless the menu explicitly marks an item as unavailable or sold out"""

EXTRACT_MENU_TOOL = {
    "name": "extract_menu",
    "description": "Extract all menu items from a restaurant menu.",
    "input_schema": {
        "type": "object",
        "properties": {
            "restaurant_name": {"type": "string"},
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "price_cents": {"type": "integer", "description": "Price in cents, e.g. $5.99 → 599"},
                                    "available": {"type": "boolean"},
                                },
                                "required": ["name", "description", "price_cents", "available"],
                            },
                        },
                    },
                    "required": ["name", "items"],
                },
            },
        },
        "required": ["restaurant_name", "sections"],
    },
}


def extract_menu_from_file(file_path: str, client: Anthropic) -> dict:
    """Send PDF or image to Claude and return structured intermediate dict."""
    mime_type, _ = mimetypes.guess_type(file_path)

    with open(file_path, "rb") as f:
        file_data = base64.standard_b64encode(f.read()).decode("utf-8")

    if mime_type == "application/pdf":
        content_block = {
            "type": "document",
            "source": {
                "type": "base64",
                "media_type": "application/pdf",
                "data": file_data,
            },
        }
    elif mime_type in SUPPORTED_IMAGE_TYPES:
        content_block = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mime_type,
                "data": file_data,
            },
        }
    else:
        raise ValueError(
            f"Unsupported file type: {mime_type}. "
            "Supported: application/pdf, image/jpeg, image/png, image/gif, image/webp"
        )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        tools=[EXTRACT_MENU_TOOL],
        tool_choice={"type": "tool", "name": "extract_menu"},
        messages=[
            {
                "role": "user",
                "content": [
                    content_block,
                    {"type": "text", "text": EXTRACTION_PROMPT},
                ],
            }
        ],
    )

    return response.content[0].input
