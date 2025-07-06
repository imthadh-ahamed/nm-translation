"""
Pydantic models for API requests and responses
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

# Constants for field descriptions
SOURCE_LANG_DESC = "Source language code"
TARGET_LANG_DESC = "Target language code"
NUM_BEAMS_DESC = "Number of beams for beam search"
MAX_LENGTH_DESC = "Maximum output length"


class TranslationRequest(BaseModel):
    """Request model for translation"""
    text: str = Field(..., min_length=1, max_length=1000, description="Text to translate")
    source_language: str = Field(default="en", description=SOURCE_LANG_DESC)
    target_language: str = Field(default="ta", description=TARGET_LANG_DESC)
    num_beams: Optional[int] = Field(default=4, ge=1, le=10, description=NUM_BEAMS_DESC)
    max_length: Optional[int] = Field(default=512, ge=10, le=1024, description=MAX_LENGTH_DESC)
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()


class TranslationResponse(BaseModel):
    """Response model for translation"""
    original_text: str = Field(..., description="Original input text")
    translated_text: str = Field(..., description="Translated output text")
    source_language: str = Field(..., description=SOURCE_LANG_DESC)
    target_language: str = Field(..., description=TARGET_LANG_DESC)
    num_beams: int = Field(..., description=NUM_BEAMS_DESC)
    confidence_score: Optional[float] = Field(None, description="Translation confidence score")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    model_info: Dict[str, Any] = Field(..., description="Model information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Translation timestamp")


class BatchTranslationRequest(BaseModel):
    """Request model for batch translation"""
    texts: List[str] = Field(..., min_items=1, max_items=10, description="List of texts to translate")
    source_language: str = Field(default="en", description=SOURCE_LANG_DESC)
    target_language: str = Field(default="ta", description=TARGET_LANG_DESC)
    num_beams: Optional[int] = Field(default=4, ge=1, le=10, description=NUM_BEAMS_DESC)
    max_length: Optional[int] = Field(default=512, ge=10, le=1024, description=MAX_LENGTH_DESC)


class BatchTranslationResponse(BaseModel):
    """Response model for batch translation"""
    translations: List[TranslationResponse] = Field(..., description="List of translation results")
    total_processing_time_ms: float = Field(..., description="Total processing time in milliseconds")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_info: Optional[Dict[str, Any]] = Field(None, description="Model information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class LanguageInfo(BaseModel):
    """Language information model"""
    code: str = Field(..., description="Language code")
    name: str = Field(..., description="Language name")
    native_name: str = Field(..., description="Native language name")


class SupportedLanguagesResponse(BaseModel):
    """Supported languages response"""
    languages: List[LanguageInfo] = Field(..., description="List of supported languages")
    total_count: int = Field(..., description="Total number of supported languages")
