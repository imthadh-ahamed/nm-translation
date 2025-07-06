
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import uvicorn
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Neural Machine Translation API",
    description="English to Tamil translation using Transformer models",
    version="1.0.0"
)

# Global variables for model and tokenizer
model = None
tokenizer = None

class TranslationRequest(BaseModel):
    text: str
    num_beams: Optional[int] = 4
    max_length: Optional[int] = 128

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    num_beams: int
    model_name: str

@app.on_event("startup")
async def load_model():
    """Load the model and tokenizer on startup"""
    global model, tokenizer

    try:
        model_path = "./saved_model"  # Update this path as needed
        logger.info(f"Loading model from {model_path}")

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

        # Move model to GPU if available
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        model.eval()

        logger.info(f"Model loaded successfully on {device}")

    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Neural Machine Translation API",
        "version": "1.0.0",
        "endpoints": {
            "/translate": "POST - Translate English text to Tamil",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(next(model.parameters()).device) if model else "none"
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """Translate English text to Tamil"""

    if not model or not tokenizer:
        raise HTTPException(status_code=500, detail="Model not loaded")

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Tokenize input
        inputs = tokenizer(
            request.text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=request.max_length
        )

        # Move inputs to the same device as model
        device = next(model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate translation
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                num_beams=request.num_beams,
                max_length=request.max_length,
                early_stopping=True,
                do_sample=False
            )

        # Decode the output
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return TranslationResponse(
            original_text=request.text,
            translated_text=translation,
            num_beams=request.num_beams,
            model_name="opus-mt-en-ta"
        )

    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
