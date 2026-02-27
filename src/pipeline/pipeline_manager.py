"""
Pipeline Manager — Orchestrates all pipeline stages for chat processing.
Stages: Input → Context → AI → Output
"""
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class PipelineManager:
    """
    Orchestrates the 4-stage chat processing pipeline.

    Flow:
        1. input_stage  — validate, sanitize, enrich
        2. context_stage — load conversation history
        3. ai_stage     — call Gemini
        4. output_stage — persist to memory, format result
    """

    def __init__(self):
        from src.pipeline.stages import (
            input_stage,
            context_stage,
            ai_stage,
            output_stage,
        )
        self._stages = [input_stage, context_stage, ai_stage, output_stage]
        logger.info("PipelineManager initialized with 4 stages.")

    async def run_chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Run the full chat pipeline.

        Args:
            message: Raw user message
            session_id: Optional session ID for continuity
            system_prompt: Optional system instruction override
            temperature: Optional generation temperature

        Returns:
            Result dict with 'response', 'session_id', 'model', etc.

        Raises:
            ValueError: If input validation fails
            Exception: On pipeline or AI errors
        """
        pipeline_start = time.perf_counter()

        # Initial context dict
        ctx: Dict[str, Any] = {
            "raw_message": message,
            "session_id": session_id,
            "system_prompt": system_prompt,
            "temperature": temperature,
            "_stages": [],
        }

        # Run each stage in sequence
        for stage in self._stages:
            stage_name = stage.__name__.split(".")[-1]
            try:
                ctx = stage.run(ctx)
            except ValueError:
                raise  # Propagate validation errors as-is
            except Exception as e:
                logger.error(f"Pipeline error at [{stage_name}]: {e}", exc_info=True)
                raise RuntimeError(f"Pipeline failed at stage '{stage_name}': {e}") from e

        total_ms = (time.perf_counter() - pipeline_start) * 1000
        result = ctx.get("result", {})
        result["total_pipeline_latency_ms"] = round(total_ms, 2)

        logger.info(
            f"Pipeline completed | session={result.get('session_id', 'n/a')} "
            f"total={total_ms:.1f}ms ai={result.get('ai_latency_ms', 0):.1f}ms "
            f"stages={result.get('pipeline_stages', [])}"
        )

        return result
