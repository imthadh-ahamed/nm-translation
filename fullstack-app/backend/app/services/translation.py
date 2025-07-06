"""
Translation service using Transformers
"""
import asyncio
import time
import torch
from typing import Optional, Dict, Any, List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import TranslationResponse

logger = get_logger(__name__)


class TranslationService:
    """Neural Machine Translation Service"""
    
    def __init__(self):
        self.model: Optional[AutoModelForSeq2SeqLM] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_info = {
            "name": "t5-small",
            "device": str(self.device),
            "loaded": False
        }
        
    def load_model(self) -> None:
        """Load the translation model"""
        try:
            logger.info(f"Loading model from {settings.MODEL_PATH}")
            
            # Try to load saved model first
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(settings.MODEL_PATH)
                logger.info("Loaded custom trained model")
                self.model_info["name"] = "custom-t5-en-ta"
            except Exception as e:
                logger.warning(f"Could not load custom model: {e}")
                logger.info("Loading fallback model: t5-small")
                self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
                self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            self.model_info.update({
                "loaded": True,
                "parameters": sum(p.numel() for p in self.model.parameters()),
                "trainable_parameters": sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            })
            
            logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise RuntimeError(f"Failed to load translation model: {e}")
    
    async def load_model_async(self) -> None:
        """Load the translation model asynchronously"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.load_model)
    
    def is_ready(self) -> bool:
        """Check if the model is loaded and ready"""
        return self.model is not None and self.tokenizer is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return self.model_info.copy()
    
    def _format_input(self, text: str, source_lang: str, target_lang: str) -> str:
        """Format input text for T5 model"""
        if source_lang == "en" and target_lang == "ta":
            return f"translate English to Tamil: {text}"
        elif source_lang == "ta" and target_lang == "en":
            return f"translate Tamil to English: {text}"
        else:
            return f"translate {source_lang} to {target_lang}: {text}"
    
    def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "ta",
        num_beams: int = 4,
        max_length: int = 512
    ) -> TranslationResponse:
        """Translate text"""
        if not self.is_ready():
            raise RuntimeError("Translation service not ready")
        
        try:
            start_time = time.time()
            
            # Format input
            input_text = self._format_input(text, source_lang, target_lang)
            
            # Tokenize
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length
            ).to(self.device)
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    num_beams=num_beams,
                    max_length=max_length,
                    early_stopping=True,
                    do_sample=False
                )
            
            # Decode output
            translated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return TranslationResponse(
                original_text=text,
                translated_text=translated_text,
                source_language=source_lang,
                target_language=target_lang,
                num_beams=num_beams,
                processing_time_ms=processing_time,
                model_info=self.model_info.copy()
            )
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            raise RuntimeError(f"Translation failed: {e}")
    
    def translate_batch(
        self,
        texts: List[str],
        source_lang: str = "en",
        target_lang: str = "ta",
        num_beams: int = 4,
        max_length: int = 512
    ) -> List[TranslationResponse]:
        """Translate multiple texts"""
        if not self.is_ready():
            raise RuntimeError("Translation service not ready")
        
        results = []
        for text in texts:
            try:
                result = self.translate(
                    text=text,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    num_beams=num_beams,
                    max_length=max_length
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error translating text '{text}': {e}")
                # Add error response
                results.append(TranslationResponse(
                    original_text=text,
                    translated_text=f"Error: {str(e)}",
                    source_language=source_lang,
                    target_language=target_lang,
                    num_beams=num_beams,
                    processing_time_ms=0,
                    model_info=self.model_info.copy()
                ))
        
        return results


# Global translation service instance
translation_service = TranslationService()
