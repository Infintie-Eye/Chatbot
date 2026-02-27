"""
Document analysis router.
POST /api/v1/analyze/document — Upload document + query → AI analysis
"""
import uuid
import time
import logging
from fastapi import APIRouter, HTTPException, File, Form, UploadFile, status

from api.models.schemas import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Analysis"])


@router.post(
    "/analyze/document",
    response_model=APIResponse,
    summary="Analyze a document with Gemini",
    description="Upload a document (PDF, DOCX, TXT, CSV, JSON, XLSX) and ask a question about it."
)
async def analyze_document(
    file: UploadFile = File(..., description="Document file"),
    query: str = Form(default="Summarize this document.", description="Your question about the document"),
    session_id: str = Form(default=None, description="Optional session ID")
):
    """Process and analyze an uploaded document."""
    from src.core.gemini_client import gemini_client
    from src.utils.file_processor import file_processor
    from config.settings import settings

    start = time.perf_counter()
    session_id = session_id or str(uuid.uuid4())

    # Read file bytes
    content_bytes = await file.read()
    file_size_kb = len(content_bytes) / 1024

    # Check size
    if len(content_bytes) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.max_file_size_mb}MB limit."
        )

    # Get extension
    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename else ""
    if ext not in settings.supported_text_formats:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported document format: {ext}. Supported: {settings.supported_text_formats}"
        )

    try:
        import io
        mock_file = io.BytesIO(content_bytes)
        mock_file.name = file.filename

        # Use a simple mock object for file_processor compatibility
        class MockUpload:
            def __init__(self, content, name, size):
                self._content = content
                self.name = name
                self.size = size
                self.type = f"application/{ext}"

            def read(self):
                return self._content

        mock = MockUpload(content_bytes, file.filename, len(content_bytes))
        success, text_content, error = file_processor.process_text_file(mock)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Could not process document: {error}"
            )

        system_instruction = (
            "You are an expert document analyst powered by Gemini 2.0 Flash. "
            "Analyze the provided document content thoroughly and answer the user's query with precision. "
            "Extract key information, provide structured insights, and reference specific sections when relevant."
        )

        analysis = gemini_client.process_document(text_content, query, ext, system_instruction)
        latency = (time.perf_counter() - start) * 1000

        return APIResponse(
            success=True,
            data={
                "analysis": analysis,
                "session_id": session_id,
                "filename": file.filename,
                "file_type": ext.upper(),
                "file_size_kb": round(file_size_kb, 2),
                "model": settings.text_model,
                "latency_ms": round(latency, 2)
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document analysis failed: {str(e)}"
        )
