# BG_Remover

A modern AI-powered background removal web application with React frontend and FastAPI backend.

## Features

- 🌐 Modern web interface accessible from any browser
- 📤 Drag & drop file upload support
- 🔄 Single or batch image processing
- 📦 Download processed images as ZIP (batch mode)
- 🐳 Docker containerized deployment
- 🚀 RESTful API for integration
- ⚡ Fast AI-powered background removal
- 📊 Real-time progress tracking

## Requirements
- Docker and Docker Compose (recommended)
- OR Node.js 18+ and Python 3.11+ (for manual setup)

---

## � Quick Start - Docker Deployment (Recommended)

### Using Docker Compose

1. Make sure Docker and Docker Compose are installed on your system

2. Clone this repository:
```bash
git clone https://github.com/CarviFPV/BG_Remover.git
cd BG_Remover
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Open your browser and navigate to:
   - **Frontend**: http://localhost:3005
   - **Backend API**: http://localhost:8005
   - **API Documentation**: http://localhost:8005/docs

5. To stop the containers:
```bash
docker-compose down
```

### Production Deployment

For production, modify the `docker-compose.yml` file:
- Change ports as needed
- Add environment variables for security
- Configure reverse proxy (nginx/traefik) if needed
---

## 🛠️ Manual Setup (Development)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8005
```

The API will be available at http://localhost:8005

### Frontend Setup

1. Navigate to the frontend directory (in a new terminal):
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
npm run dev
```

The web app will be available at http://localhost:3005

---

## 📡 API Endpoints

### POST `/remove-background`
Remove background from a single image
- **Input**: Single image file (PNG/JPEG)
- **Output**: Processed image with transparent background

### POST `/remove-background-batch`
Remove background from multiple images
- **Input**: Multiple image files (PNG/JPEG)
- **Output**: ZIP file containing all processed images

### GET `/health`
Health check endpoint for monitoring

### GET `/docs`
Interactive API documentation (Swagger UI)

---

## 📁 Project Structure

```
BG_Remover/
├── backend/                # FastAPI backend
│   ├── main.py            # API endpoints
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Backend container
│   └── .dockerignore
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   ├── App.css       # Styling
│   │   └── main.jsx      # Entry point
│   ├── package.json      # Node dependencies
│   ├── vite.config.js    # Vite configuration
│   ├── Dockerfile        # Frontend container
│   ├── nginx.conf        # Nginx configuration
│   └── .dockerignore
├── docker-compose.yml     # Docker orchestration
└── README.md
```

---

## How it Works

The application uses the `rembg` library, which employs a U2-Net neural network model to automatically detect and remove backgrounds from images.

The React frontend communicates with the FastAPI backend via REST API to process images using AI.

## Technology Stack

- **Frontend**: React 18, Vite, Axios
- **Backend**: FastAPI, Python 3.11
- **AI**: rembg with ONNX Runtime
- **Image Processing**: Pillow (PIL)
- **Deployment**: Docker, Nginx

## Notes

- The first run may take longer as rembg downloads the AI model (~176MB)
- Supports PNG, JPG, and JPEG image formats
- Processed images have transparent backgrounds (PNG format)
- Docker deployment includes health checks and auto-restart
- Frontend runs on port 3005, backend API on port 8005
- Maximum upload size: 1000MB (1GB) for batch processing
- Processing timeout: 10 minutes for large batches

## License

See the LICENSE file for details.
