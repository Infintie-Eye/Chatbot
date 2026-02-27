"""
Image analysis router.
POST /api/v1/analyze/image — Upload image + prompt → Gemini vision analysis
"""
import uuid
import time
import logging
from fastapi import APIRouter, HTTPException, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from api.models.schemas import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Analysis"])


@router.post(
    "/analyze/image",
    response_model=APIResponse,
    summary="Analyze an image with Gemini Vision",
    description="Upload an image file and provide a prompt. Returns a detailed AI analysis."
)
async def analyze_image(
    file: UploadFile = File(..., description="Image file (jpg, png, gif, webp, bmp)"),
    prompt: str = Form(default="Describe this image in detail.", description="Analysis prompt"),
    session_id: str = Form(default=None, description="Optional session ID")
):
    """Analyze an uploaded image using Gemini Vision."""
    from src.core.gemini_client import gemini_client
    from src.utils.file_processor import file_processor
    from config.settings import settings

    start = time.perf_counter()
    session_id = session_id or str(uuid.uuid4())

    # Validate file type
    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename else ""
    if ext not in settings.supported_image_formats:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported image format: {ext}. Supported: {settings.supported_image_formats}"
        )

    # Validate size
    content = await file.read()
    if len(content) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.max_file_size_mb}MB limit."
        )

    try:
        import io
        from PIL import Image as PILImage

        image = PILImage.open(io.BytesIO(content))
        if image.mode != "RGB":
            image = image.convert("RGB")

        system_instruction = (
            "You are an expert image analyst powered by Gemini 2.0 Flash. "
            "Provide detailed, accurate, and insightful analysis of the provided image. "
            "Be descriptive about objects, colors, composition, context, and any text visible."
        )

        analysis = gemini_client.analyze_image(image, prompt, system_instruction)
        latency = (time.perf_counter() - start) * 1000

        return APIResponse(
            success=True,
            data={
                "analysis": analysis,
                "session_id": session_id,
                "filename": file.filename,
                "image_size": {"width": image.width, "height": image.height},
                "model": settings.vision_model,
                "latency_ms": round(latency, 2)
            }
        )

    except Exception as e:
        logger.error(f"Image analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image analysis failed: {str(e)}"
        )
