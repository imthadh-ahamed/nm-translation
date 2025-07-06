import axios from 'axios';
import {
  TranslationRequest,
  TranslationResponse,
  BatchTranslationRequest,
  BatchTranslationResponse,
  SupportedLanguagesResponse,
  HealthResponse,
  ApiError
} from './types';

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const apiError: ApiError = {
      error: error.response?.data?.error || 'API Error',
      message: error.response?.data?.message || error.message || 'An error occurred',
      details: error.response?.data?.details
    };
    
    console.error('API Error:', apiError);
    return Promise.reject(apiError);
  }
);

// API Functions
export const translationApi = {
  // Translate single text
  async translate(request: TranslationRequest): Promise<TranslationResponse> {
    const response = await apiClient.post('/api/v1/translate', request);
    return response.data;
  },

  // Translate multiple texts
  async translateBatch(request: BatchTranslationRequest): Promise<BatchTranslationResponse> {
    const response = await apiClient.post('/api/v1/translate/batch', request);
    return response.data;
  },

  // Get supported languages
  async getSupportedLanguages(): Promise<SupportedLanguagesResponse> {
    const response = await apiClient.get('/api/v1/languages');
    return response.data;
  },

  // Health check
  async getHealth(): Promise<HealthResponse> {
    const response = await apiClient.get('/api/v1/health');
    return response.data;
  },

  // Get model info
  async getModelInfo(): Promise<Record<string, unknown>> {
    const response = await apiClient.get('/api/v1/model/info');
    return response.data;
  }
};

export default apiClient;
