import tempfile

from fastapi import APIRouter, HTTPException, UploadFile

from app.api.dependencies import client, menu
from app.api.schemas import MenuParseResponse
from app.models.menu import MenuItem
from app.services.menu_parser.pdf_extractor import extract_menu_from_pdf
from app.services.menu_parser.schema_converter import convert_to_menu_items

router = APIRouter()


@router.get("/menu", response_model=list[MenuItem])
async def get_menu_items() -> list[MenuItem]:
    return menu


@router.post("/menu/parse", response_model=MenuParseResponse)
async def parse_menu(file: UploadFile) -> MenuParseResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    contents = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        intermediate = extract_menu_from_pdf(tmp_path, client)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to parse PDF: {e}")

    items = convert_to_menu_items(intermediate)

    return MenuParseResponse(
        section_count=len(intermediate.get("sections", [])),
        items=items,
    )
