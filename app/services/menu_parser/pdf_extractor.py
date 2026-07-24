import base64
import json

from anthropic import Anthropic

EXTRACTION_PROMPT = """Extract all menu items from this restaurant menu PDF.

Output JSON in exactly this format:
{
  "restaurant_name": "...",
  "sections": [
    {
      "name": "Section Name",
      "items": [
        {
          "name": "Item Name",
          "description": "Item description or empty string",
          "price": "$X.XX",
          "available": true
        }
      ]
    }
  ]
}

Rules:
- Include every item visible on the menu
- Use empty string for missing descriptions
- Keep prices exactly as shown (e.g. "$5.99")
- Set available to true unless the menu explicitly marks an item as unavailable
- Output only valid JSON, no other text"""


def extract_menu_from_pdf(pdf_path: str, client: Anthropic) -> dict:
    """Send PDF to Claude Vision and return structured intermediate dict."""
    with open(pdf_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": EXTRACTION_PROMPT,
                    },
                ],
            }
        ],
    )

    return json.loads(response.content[0].text)
