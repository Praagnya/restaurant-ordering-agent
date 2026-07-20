from unittest.mock import MagicMock

import pytest
from anthropic import Anthropic

from app.agent.parser import parse_order
from app.models.order import ParsedOrder, RequestedItem, RequestedModifier


def _mock_client(parsed_order: ParsedOrder) -> Anthropic:
    client = MagicMock(spec=Anthropic)
    response = MagicMock()
    response.content = [MagicMock(text=parsed_order.model_dump_json())]
    client.messages.create.return_value = response
    return client


class TestParseOrder:
    def test_returns_parsed_order(self):
        expected = ParsedOrder(items=[RequestedItem(name="fries")])
        result = parse_order("give me fries", _mock_client(expected))
        assert result == expected

    def test_complex_order_preserved(self):
        expected = ParsedOrder(items=[
            RequestedItem(name="big mac", quantity=2),
            RequestedItem(
                name="chicken sandwich",
                modifiers=[RequestedModifier(action="remove", name="onions")],
            ),
            RequestedItem(name="medium fries"),
        ])
        result = parse_order(
            "two big macs, chicken sandwich no onions, medium fries",
            _mock_client(expected),
        )
        assert result == expected

    def test_api_called_exactly_once(self):
        client = _mock_client(ParsedOrder(items=[]))
        parse_order("anything", client)
        assert client.messages.create.call_count == 1

    def test_customer_text_sent_to_api(self):
        client = _mock_client(ParsedOrder(items=[]))
        parse_order("two big macs please", client)
        messages = client.messages.create.call_args.kwargs["messages"]
        assert any("two big macs please" in msg["content"] for msg in messages)

    def test_correct_model_used(self):
        client = _mock_client(ParsedOrder(items=[]))
        parse_order("a burger", client)
        assert client.messages.create.call_args.kwargs["model"] == "claude-opus-4-8"

    def test_raises_on_invalid_json(self):
        client = MagicMock(spec=Anthropic)
        response = MagicMock()
        response.content = [MagicMock(text="not valid json at all")]
        client.messages.create.return_value = response
        with pytest.raises(Exception):
            parse_order("something", client)
