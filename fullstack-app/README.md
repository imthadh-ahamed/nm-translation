# Neural Machine Translation System

A full-stack Neural Machine Translation application for English↔Tamil translation using Transformer models.

## Features

- **Real-time Translation**: English to Tamil and Tamil to English translation
- **Modern UI**: Built with Next.js and Tailwind CSS
- **AI-Powered**: Uses T5 transformer model fine-tuned for English-Tamil translation
- **Production Ready**: FastAPI backend with proper error handling and logging
- **Health Monitoring**: System health and model status monitoring
- **Advanced Options**: Configurable beam search and output length
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Modern icon library
- **Axios**: HTTP client for API calls

### Backend
- **FastAPI**: Modern Python web framework
- **Transformers**: Hugging Face transformer models
- **PyTorch**: Deep learning framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

## Architecture

```
fullstack-app/
├── frontend/                 # Next.js application
│   ├── app/                 # App Router pages
│   ├── components/          # React components
│   ├── lib/                 # Utilities and API client
│   └── public/              # Static assets
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration and logging
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── saved_model/        # Trained model files
│   └── tests/              # Test files
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd fullstack-app/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python -m app.main
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd fullstack-app/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy environment variables:
   ```bash
   cp .env.example .env.local
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Translation
- `POST /api/v1/translate` - Translate single text
- `POST /api/v1/translate/batch` - Translate multiple texts

### System
- `GET /api/v1/health` - Health check
- `GET /api/v1/languages` - Supported languages
- `GET /api/v1/model/info` - Model information

### Example API Usage

```bash
# Single translation
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "source_language": "en",
    "target_language": "ta"
  }'

# Health check
curl "http://localhost:8000/api/v1/health"
```

## Model Information

The system uses a T5-small model fine-tuned on English-Tamil parallel data:
- **Base Model**: google/t5-small
- **Training Data**: Helsinki-NLP opus datasets
- **Languages**: English (en) ↔ Tamil (ta)
- **Architecture**: Encoder-Decoder Transformer

## Development

### Frontend Development
```bash
cd fullstack-app/frontend
npm run dev      # Start development server
npm run build    # Build for production
npm run lint     # Run ESLint
```

### Backend Development
```bash
cd fullstack-app/backend
python -m app.main              # Start development server
python -m pytest               # Run tests
python -m black app/            # Code formatting
python -m flake8 app/           # Linting
```

## Deployment

### Using Docker

1. Build and run the backend:
   ```bash
   cd fullstack-app/backend
   docker build -t nmt-backend .
   docker run -p 8000:8000 nmt-backend
   ```

2. Build and run the frontend:
   ```bash
   cd fullstack-app/frontend
   docker build -t nmt-frontend .
   docker run -p 3000:3000 nmt-frontend
   ```

### Production Considerations

- Set up proper environment variables
- Configure CORS for production domains
- Use a reverse proxy (nginx)
- Set up monitoring and logging
- Configure model caching and optimization
- Consider using GPU for better performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Hugging Face for the Transformers library
- Helsinki-NLP for the translation datasets
- Google for the T5 model architecture
