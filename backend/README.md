# ABP AI Video Generation Backend

A comprehensive AI-powered video generation system with voice synthesis, music generation, post-processing, and quality control.

## 🚀 Features

### Core Services
- **Voice Generation**: ElevenLabs & OpenAI TTS integration
- **Music Generation**: Suno API & MusicGen support
- **Video Post-Processing**: Frame interpolation (RIFE) & upscaling (Real-ESRGAN)
- **Quality Control**: Automated compliance & technical checks
- **CDN Storage**: Cloudflare R2 & AWS S3 support
- **Payment Processing**: Stripe integration with credit system

### API Endpoints

#### Voice Generation
- `POST /api/v1/generate/voice` - Generate voice-over from text
- `GET /api/v1/voice/options` - Get available voice options

#### Music Generation
- `POST /api/v1/generate/music` - Generate music from prompt
- `GET /api/v1/music/presets` - Get music generation presets

#### Video Processing
- `POST /api/v1/process/video` - Post-process video with enhancements
- `GET /api/v1/video/info/{video_key}` - Get video information

#### Quality Control
- `POST /api/v1/qc/check` - Perform quality control check

#### Payment
- `POST /api/v1/payment/checkout` - Create Stripe checkout session
- `POST /api/v1/payment/webhook` - Handle Stripe webhooks
- `GET /api/v1/payment/packages` - Get credit packages

#### Storage
- `POST /api/v1/storage/upload` - Upload file to CDN
- `GET /api/v1/storage/list` - List files in storage
- `GET /api/v1/storage/stats` - Get storage statistics

## 📋 Requirements

- Python 3.10+
- Docker & Docker Compose
- NVIDIA GPU (for video processing)
- PostgreSQL 15+
- Redis 7+

## 🛠️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/alovladi007/abp-interactive-learning.git
cd abp-interactive-learning/backend
```

### 2. Environment Variables
Create a `.env` file in the backend directory:

```env
# Application
SECRET_KEY=your-secret-key-here
DEBUG=false

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/abp_video

# AI Services
OPENAI_API_KEY=sk-...
ELEVEN_API_KEY=your-elevenlabs-key
SUNO_API_KEY=your-suno-key

# Storage (Cloudflare R2)
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET=abp-videos

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f api
```

### 4. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the API server
python main.py
```

## 🏗️ Architecture

```mermaid
graph TD
    Client[Client App] --> API[FastAPI Server]
    API --> Redis[(Redis Cache)]
    API --> Postgres[(PostgreSQL)]
    API --> CDN[Cloudflare R2/S3]
    
    API --> Voice[Voice Service]
    Voice --> ElevenLabs[ElevenLabs API]
    Voice --> OpenAI[OpenAI TTS]
    
    API --> Music[Music Service]
    Music --> Suno[Suno API]
    
    API --> PostProc[Post Processing]
    PostProc --> RIFE[RIFE Interpolation]
    PostProc --> ESRGAN[Real-ESRGAN]
    
    API --> QC[Quality Control]
    QC --> OpenAIMod[OpenAI Moderation]
    
    API --> Payment[Stripe Service]
    Payment --> Stripe[Stripe API]
    
    Celery[Celery Workers] --> Redis
    Celery --> PostProc
```

## 📊 Credit System

### Credit Costs
- Video Generation: 2 credits/second
- Voice Generation: 5 credits/minute
- Music Generation: 3 credits/minute
- 2x Upscaling: 10 credits
- 4x Upscaling: 20 credits
- Frame Interpolation: 15 credits
- Quality Check: 1 credit

### Credit Packages
- **Starter**: 100 credits for $9.99
- **Pro**: 500 credits for $39.99 (20% savings)
- **Enterprise**: 2000 credits for $149.99 (25% savings)

## 🔧 API Usage Examples

### Generate Voice
```bash
curl -X POST http://localhost:8000/api/v1/generate/voice \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to our AI video platform",
    "voice_id": "narrator",
    "emotion": "friendly",
    "tempo": 1.0
  }'
```

### Generate Music
```bash
curl -X POST http://localhost:8000/api/v1/generate/music \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Uplifting corporate background music",
    "duration": 60,
    "genre": "corporate",
    "mood": "uplifting"
  }'
```

### Process Video
```bash
curl -X POST http://localhost:8000/api/v1/process/video \
  -H "Content-Type: application/json" \
  -d '{
    "video_key": "videos/sample.mp4",
    "interpolation_factor": 2,
    "upscale_factor": 2,
    "target_fps": 60
  }'
```

## 🚨 Quality Control

The system performs automated checks for:
- **Technical Requirements**: FPS, resolution, duration
- **Content Moderation**: Banned keywords, OpenAI moderation
- **Visual Quality**: Brightness, blur detection
- **Frame Analysis**: Frozen frames, duplicates

## 🔐 Security

- JWT authentication (to be implemented)
- Rate limiting per user
- Input validation and sanitization
- Stripe webhook signature verification
- Secure file uploads with type validation

## 📈 Monitoring

- Health check endpoint: `/health`
- Flower dashboard: `http://localhost:5555`
- Prometheus metrics (coming soon)
- Sentry error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/alovladi007/abp-interactive-learning/issues)
- Email: support@abplearning.com