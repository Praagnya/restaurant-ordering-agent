import tempfile

from fastapi import APIRouter, Form, HTTPException, UploadFile

from app.api.dependencies import client, menu
from app.api.schemas import MenuParseResponse
from app.models.menu import MenuItem
from app.services.parser.extractor import extract_menu_from_file
from app.services.parser.schema_converter import convert_to_menu_items

router = APIRouter()

SUPPORTED_CONTENT_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


@router.get("/menu", response_model=list[MenuItem])
async def get_menu_items() -> list[MenuItem]:
    return menu


@router.post("/menu/parse", response_model=MenuParseResponse)
async def parse_menu(
    file: UploadFile,
    restaurant_name: str | None = Form(None),
) -> MenuParseResponse:
    if file.content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Accepted: {', '.join(SUPPORTED_CONTENT_TYPES)}",
        )

    suffix = SUPPORTED_CONTENT_TYPES[file.content_type]
    contents = await file.read()

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        intermediate = extract_menu_from_file(tmp_path, client)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse menu: {e}")

    items = convert_to_menu_items(intermediate)

    resolved_name = (
        restaurant_name
        or intermediate.get("restaurant_name")
        or "Unnamed Restaurant"
    )

    return MenuParseResponse(
        restaurant_name=resolved_name,
        section_count=len(intermediate.get("sections", [])),
        items=items,
    )
