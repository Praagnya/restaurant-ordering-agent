# Restaurant Order Agent

## Project goal

Build a production-style agentic AI system that takes natural-language restaurant
orders and carries them through to completion — menu lookup, cart creation, upsell,
confirmation, payment, and POS submission.

This project demonstrates the full stack of skills required for a Junior AI Engineer
role: agentic systems with tool use, deterministic ML-backed services, LLM API
integration, structured outputs, Pydantic validation, and a path to deployment.

Example:

Customer:
"Give me two chicken sandwiches, one without onions, and add fries."

Expected structured interpretation:

- One regular chicken sandwich
- One chicken sandwich without onions
- One order of fries

The final system will support:

1. Order extraction
2. Menu search
3. Modifier validation
4. Availability checks
5. Cart creation
6. Upsell recommendations
7. Total calculation
8. Customer confirmation
9. Payment
10. POS submission

## Current scope

Only implement the current milestone requested by the developer.

Do not implement the entire application at once.

The first milestone is:

Customer text
→ ParsedOrder (structured extraction via LLM with tool use)
→ Pydantic validation
→ ResolvedOrder (menu lookup via deterministic services)

Do not add voice, payment, POS integration, databases, or deployment until
explicitly requested.

## Architecture principles

- The agent uses Codex with tool use to orchestrate the ordering flow.
- Services (menu search, cart, pricing, payment) are exposed as tools the agent calls.
- Use deterministic Python code for menu validation, pricing, carts, payment,
  and POS operations — never let the LLM compute these.
- Validate all LLM output with Pydantic.
- Never allow the LLM to invent prices, menu item IDs, modifier IDs, availability,
  or payment results.
- Keep business logic in services, separate from agent orchestration.
- LangGraph will orchestrate multi-step flows once single-agent tool use is working.
- Represent money as integer cents, not floating-point dollars.
- Require explicit customer confirmation before payment.
- Payment and POS operations must support idempotency.

## Milestones

1. **Text → structured order** (current): LLM extracts a ParsedOrder, services resolve it against the menu.
2. **Tool-calling agent**: Wrap services as Codex tools; agent drives the full ordering conversation.
3. **LangGraph orchestration**: Replace single-agent loop with a stateful LangGraph graph.
4. **Deployment**: Containerize and expose via FastAPI; deploy to a cloud provider.
5. **Observability**: Add eval and tracing (Langfuse or LangSmith).
6. **Voice**: Add speech-to-text input layer.

## Development workflow

For every feature:

1. Define the input and output models.
2. Define the function contract.
3. Write tests.
4. Implement only that function.
5. Run the tests.
6. Explain any non-obvious code.
7. Do not proceed to the next feature automatically.

Before creating or editing multiple files, explain the proposed changes.

## Coding standards

- Use Python 3.12.
- Use type annotations for all public functions.
- Use Pydantic v2 models.
- Use `Field(default_factory=list)` for mutable defaults.
- Prefer small functions with one responsibility.
- Use descriptive names.
- Do not use `eval`.
- Do not catch broad exceptions without re-raising or logging.
- Do not silently ignore invalid input.
- Avoid unnecessary frameworks and abstractions.
- Use async code only for actual I/O operations.
- Use docstrings for public services and complex business rules.

## Testing standards

- Use pytest.
- Test successful behavior and failure cases.
- Avoid weak tests such as checking only that a result is not `None`.
- Every business rule should have at least one test.
- Do not modify tests merely to make failing code pass unless the expected
  behavior itself is incorrect.

## Repository structure

```text
app/
├── models/        # Pydantic models
├── services/      # Deterministic business logic (exposed as agent tools)
├── agent/         # LLM agent, tool definitions, prompt templates
└── repositories/  # Data access (menu, orders)

tests/
```
