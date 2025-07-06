# Neural Machine Translation (NMT) System

A full-stack Neural Machine Translation system for English ↔ Tamil translation using Transformer models (T5). The system features a Python FastAPI backend and a Next.js frontend, designed for production deployment with Docker support.

## 🌟 Features

- **Bidirectional Translation**: English to Tamil and Tamil to English
- **Transformer Model**: Based on T5-small architecture with custom training capabilities
- **Modern Web Interface**: Responsive Next.js frontend with Tailwind CSS
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Real-time Translation**: Fast inference with configurable beam search
- **Batch Processing**: Support for multiple text translations
- **Model Management**: Custom model training and deployment
- **Health Monitoring**: API health checks and model status
- **Docker Support**: Containerized deployment with docker-compose
- **Development Tools**: Hot reload, debugging, and testing support

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Docker & Docker Compose** (optional, for containerized deployment)
- **CUDA-compatible GPU** (optional, for faster training/inference)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd nm-translation
   ```

2. **Start the Backend**
   ```bash
   cd fullstack-app/backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Start the Frontend** (in a new terminal)
   ```bash
   cd fullstack-app/frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🧠 Model Training

The system supports custom model training using the included Jupyter notebook:

1. **Open the training notebook**
   ```bash
   cd ml
   jupyter notebook nm-translation.ipynb
   ```

2. **Follow the notebook sections**:
   - Data loading and preprocessing
   - Model configuration and training
   - Evaluation and metrics
   - Model export for deployment

3. **Deploy trained model**:
   - Save model to `fullstack-app/backend/saved_model/`
   - Restart the backend service

## 🔧 Configuration

### Backend Configuration

Environment variables in `fullstack-app/backend/.env`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Model Configuration
MODEL_PATH=./saved_model
MODEL_NAME=t5-small

# API Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

### Frontend Configuration

Environment variables in `fullstack-app/frontend/.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests

```bash
cd fullstack-app/backend
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd fullstack-app/frontend
npm test
```

## 📊 Performance

- **Translation Speed**: ~100-500ms per sentence (CPU)
- **Model Size**: ~250MB (T5-small)
- **Memory Usage**: ~2-4GB RAM
- **Concurrent Users**: 50+ (with proper scaling)

## 🔍 Development Scripts

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload

# Run tests
python -m pytest

# Format code
black app/ tests/
isort app/ tests/
```

### Frontend

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint and format
npm run lint
```

## 🛠️ Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure model files are in `saved_model/` directory
   - Check model compatibility with transformers version

2. **CORS Errors**
   - Verify `ALLOWED_ORIGINS` in backend configuration
   - Check frontend API URL configuration

3. **Port Conflicts**
   - Backend: Change port in configuration
   - Frontend: Next.js will auto-detect available ports

4. **Memory Issues**
   - Reduce batch size in model configuration
   - Use CPU instead of GPU if memory limited

### Performance Optimization

- **Model**: Use quantized models for lower memory usage
- **Backend**: Implement model caching and connection pooling
- **Frontend**: Enable API response caching
- **Infrastructure**: Use load balancers and horizontal scaling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Add tests for new features
- Update documentation for API changes
- Use conventional commit messages