"""
Translation API routes
"""
import time
from typing import List
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models.schemas import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    HealthResponse,
    ErrorResponse,
    SupportedLanguagesResponse,
    LanguageInfo
)
from app.services.translation import translation_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/translate",
    response_model=TranslationResponse,
    summary="Translate text",
    description="Translate text from source language to target language"
)
async def translate_text(request: TranslationRequest) -> TranslationResponse:
    """Translate text endpoint"""
    try:
        if not translation_service.is_ready():
            raise HTTPException(
                status_code=503,
                detail="Translation service not ready. Model is still loading."
            )
        
        result = translation_service.translate(
            text=request.text,
            source_lang=request.source_language,
            target_lang=request.target_language,
            num_beams=request.num_beams,
            max_length=request.max_length
        )
        
        logger.info(f"Translated text: {request.text[:50]}...")
        return result
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/translate/batch",
    response_model=BatchTranslationResponse,
    summary="Translate multiple texts",
    description="Translate multiple texts in a single request"
)
async def translate_batch(request: BatchTranslationRequest) -> BatchTranslationResponse:
    """Batch translation endpoint"""
    try:
        if not translation_service.is_ready():
            raise HTTPException(
                status_code=503,
                detail="Translation service not ready. Model is still loading."
            )
        
        start_time = time.time()
        
        results = translation_service.translate_batch(
            texts=request.texts,
            source_lang=request.source_language,
            target_lang=request.target_language,
            num_beams=request.num_beams,
            max_length=request.max_length
        )
        
        total_time = (time.time() - start_time) * 1000
        
        logger.info(f"Batch translated {len(request.texts)} texts")
        
        return BatchTranslationResponse(
            translations=results,
            total_processing_time_ms=total_time
        )
        
    except Exception as e:
        logger.error(f"Batch translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the translation service"
)
async def health_check() -> HealthResponse:
    """Health check endpoint"""
    model_info = translation_service.get_model_info()
    
    return HealthResponse(
        status="healthy" if translation_service.is_ready() else "loading",
        version="1.0.0",
        model_loaded=translation_service.is_ready(),
        model_info=model_info
    )


@router.get(
    "/languages",
    response_model=SupportedLanguagesResponse,
    summary="Get supported languages",
    description="Get list of supported languages for translation"
)
async def get_supported_languages() -> SupportedLanguagesResponse:
    """Get supported languages endpoint"""
    languages = [
        LanguageInfo(code="en", name="English", native_name="English"),
        LanguageInfo(code="ta", name="Tamil", native_name="தமிழ்")
    ]
    
    return SupportedLanguagesResponse(
        languages=languages,
        total_count=len(languages)
    )


@router.get(
    "/model/info",
    summary="Get model information",
    description="Get detailed information about the loaded model"
)
async def get_model_info():
    """Get model information endpoint"""
    if not translation_service.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    return translation_service.get_model_info()
