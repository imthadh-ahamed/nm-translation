// API Types and Interfaces
export interface TranslationRequest {
  text: string;
  source_language: string;
  target_language: string;
  num_beams?: number;
  max_length?: number;
}

export interface TranslationResponse {
  original_text: string;
  translated_text: string;
  source_language: string;
  target_language: string;
  num_beams: number;
  confidence_score?: number;
  processing_time_ms: number;
  model_info: {
    name: string;
    device: string;
    loaded: boolean;
  };
  timestamp: string;
}

export interface BatchTranslationRequest {
  texts: string[];
  source_language: string;
  target_language: string;
  num_beams?: number;
  max_length?: number;
}

export interface BatchTranslationResponse {
  translations: TranslationResponse[];
  total_processing_time_ms: number;
}

export interface LanguageInfo {
  code: string;
  name: string;
  native_name: string;
}

export interface SupportedLanguagesResponse {
  languages: LanguageInfo[];
  total_count: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  model_loaded: boolean;
  model_info: {
    name: string;
    device: string;
    loaded: boolean;
    parameters?: number;
    trainable_parameters?: number;
  };
}

export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, unknown>;
}
