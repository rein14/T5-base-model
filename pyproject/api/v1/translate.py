from fastapi import APIRouter
from .schemes.translate import SupportedLanguages
from .core.config import api_router
from fastapi.responses import RedirectResponse
from transformers import T5ForConditionalGeneration, T5Tokenizer

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small", return_dict=True)

router = api_router

@router.get("/", include_in_schema=False)
async def root():
    """Root"""
    return RedirectResponse(url="/docs")


@router.post("/translate/")
async def translate_fn(
    source_language: SupportedLanguages,
    destination_language: SupportedLanguages,
    input_text,
):
    """Translate text base defined source to destination"""
    input_ids = tokenizer(
        f"translate {source_language} to {destination_language}: {input_text}", return_tensors="pt"
    ).input_ids
    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return decoded
