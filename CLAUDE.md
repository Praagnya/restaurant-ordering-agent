# Restaurant Order Agent

## Project goal

Build a production-style restaurant ordering agent that converts natural-language
customer requests into validated orders.

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
→ structured order
→ Pydantic validation

Do not add LangGraph, voice, payment, POS integration, databases, or APIs until
explicitly requested.

## Architecture principles

- Use the LLM only for natural-language understanding and response generation.
- Use deterministic Python code for menu validation, pricing, carts, payment,
  and POS operations.
- Validate all LLM output with Pydantic.
- Never allow the LLM to invent prices, menu item IDs, modifier IDs, availability,
  or payment results.
- Keep business logic separate from orchestration.
- LangGraph will eventually orchestrate tested service functions.
- Represent money as integer cents, not floating-point dollars.
- Require explicit customer confirmation before payment.
- Payment and POS operations must support idempotency.

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
├── models/
├── services/
├── agent/
└── repositories/

tests/